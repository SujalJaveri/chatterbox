"""
Chatterbox Turbo TTS - Command Line & Scripting Interface
Supports single prompt generation, batch processing, and multiple takes.
"""

import argparse
import os
import sys
from pathlib import Path
import torch
import torchaudio as ta

# Ensure checkpoints exist before importing Chatterbox
from download_models import ensure_models

try:
    from chatterbox.tts_turbo import ChatterboxTurboTTS
except ImportError:
    print("[ERROR] chatterbox-tts is not installed in this environment.")
    print("Please run: pip install -r requirements.txt")
    sys.exit(1)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Chatterbox Turbo TTS - AI Voice Generator & Voice Cloner"
    )
    parser.add_argument(
        "--text",
        "-t",
        type=str,
        default="Who the hell are you",
        help="Text prompt to generate speech for.",
    )
    parser.add_argument(
        "--voice",
        "-v",
        type=str,
        default="voice.wav",
        help="Path to reference audio file (.wav or .mp3) for zero-shot voice cloning.",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default="output.wav",
        help="Path where generated audio will be saved.",
    )
    parser.add_argument(
        "--batch-file",
        "-b",
        type=str,
        default=None,
        help="Path to a text file containing one prompt per line for batch generation.",
    )
    parser.add_argument(
        "--takes",
        type=int,
        default=1,
        help="Number of different takes / variations to generate for the text.",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.8,
        help="Sampling temperature (0.1 - 1.2). Default: 0.8",
    )
    parser.add_argument(
        "--exaggeration",
        type=float,
        default=0.0,
        help="Emotion/expression exaggeration (0.0 - 1.0). Default: 0.0",
    )
    parser.add_argument(
        "--device",
        type=str,
        default=None,
        help="Compute device ('cuda' or 'cpu'). Defaults to auto-detect.",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Determine compute device
    if args.device:
        device = args.device
    else:
        device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Device: {device.upper()}")

    # Ensure model weights are ready
    ckpt_dir = ensure_models()

    # Load model
    print("Loading Chatterbox Turbo TTS model...")
    model = ChatterboxTurboTTS.from_local(ckpt_dir, device=device)
    print("Model loaded successfully!")

    # Verify voice reference file
    voice_path = Path(args.voice)
    if voice_path.exists():
        print(f"Conditioning on reference voice: {voice_path.name}")
        model.prepare_conditionals(str(voice_path), exaggeration=args.exaggeration)
    else:
        print(f"Notice: Reference audio '{args.voice}' not found. Using default built-in voice.")

    # Determine prompt list
    if args.batch_file:
        batch_path = Path(args.batch_file)
        if not batch_path.exists():
            print(f"[ERROR] Batch file not found: {batch_path}")
            sys.exit(1)
        with open(batch_path, "r", encoding="utf-8") as f:
            prompts = [line.strip() for line in f if line.strip()]
        print(f"Loaded {len(prompts)} prompts from {batch_path.name}")

        out_dir = Path("outputs")
        out_dir.mkdir(exist_ok=True)
        for idx, p in enumerate(prompts, start=1):
            print(f"Generating [{idx}/{len(prompts)}]: {p[:40]}...")
            wav = model.generate(p, temperature=args.temperature)
            save_path = out_dir / f"output_{idx:03d}.wav"
            ta.save(str(save_path), wav, model.sr)
            print(f"  -> Saved to {save_path}")
        print("Batch generation completed successfully!")
        return

    # Single text generation or takes
    if args.takes > 1:
        out_dir = Path("outputs")
        out_dir.mkdir(exist_ok=True)
        base_name = Path(args.output).stem
        for take in range(1, args.takes + 1):
            print(f"Generating take {take}/{args.takes}...")
            wav = model.generate(args.text, temperature=args.temperature)
            save_path = out_dir / f"{base_name}_take_{take}.wav"
            ta.save(str(save_path), wav, model.sr)
            print(f"  -> Saved to {save_path}")
        print(f"Generated {args.takes} takes in '{out_dir}'!")
        return

    # Standard single output
    print(f"Generating speech for: \"{args.text}\"")
    wav = model.generate(args.text, temperature=args.temperature)
    ta.save(args.output, wav, model.sr)
    print(f"Audio successfully saved to: {args.output}")


if __name__ == "__main__":
    main()