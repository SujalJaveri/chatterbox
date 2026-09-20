"""
Chatterbox Turbo TTS - Web UI Application
Powered by Gradio. Provides single generation, zero-shot voice cloning,
and multi-output batch synthesis with an in-browser audio player.
"""

import os
import sys
import tempfile
import time
from pathlib import Path

import gradio as gr
import spaces
import torch
import torchaudio as ta

from download_models import ensure_models

try:
    from chatterbox.tts_turbo import ChatterboxTurboTTS
except ImportError:
    print("[ERROR] chatterbox-tts is not installed in this environment.")
    print("Please run: pip install -r requirements.txt")
    sys.exit(1)

# Ensure models are ready
CKPT_DIR = ensure_models()
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Loading Chatterbox Turbo TTS on {DEVICE.upper()}...")
MODEL = ChatterboxTurboTTS.from_local(CKPT_DIR, device=DEVICE)
print("Model loaded and ready!")

# Default reference voice path
DEFAULT_VOICE = Path("voice.wav")
CURRENT_VOICE_FILE = None


def get_cached_conditionals(voice_file, exaggeration=0.0):
    """Loads and conditions the reference audio only if it changed."""
    global CURRENT_VOICE_FILE
    if voice_file and os.path.exists(voice_file):
        target_path = str(voice_file)
        MODEL.prepare_conditionals(target_path, exaggeration=exaggeration)
        CURRENT_VOICE_FILE = target_path
    elif DEFAULT_VOICE.exists():
        if CURRENT_VOICE_FILE != str(DEFAULT_VOICE):
            MODEL.prepare_conditionals(str(DEFAULT_VOICE), exaggeration=exaggeration)
            CURRENT_VOICE_FILE = str(DEFAULT_VOICE)


@spaces.GPU
def generate_single_voice(text, voice_audio, temperature, exaggeration):
    """Generates audio for a single prompt."""
    if not text or not text.strip():
        return None, "Please enter some text to generate speech."

    start_time = time.time()
    try:
        get_cached_conditionals(voice_audio, exaggeration=exaggeration)
        wav = MODEL.generate(text.strip(), temperature=temperature)

        # Save to temporary wav file for Gradio audio player
        temp_out = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        temp_out_path = temp_out.name
        temp_out.close()

        ta.save(temp_out_path, wav, MODEL.sr)
        elapsed = time.time() - start_time
        return temp_out_path, f"Generated successfully in {elapsed:.2f}s!"
    except Exception as e:
        return None, f"Error during generation: {str(e)}"


@spaces.GPU
def generate_batch_voice(lines_text, voice_audio, temperature, exaggeration):
    """Generates audio for multiple lines or takes."""
    lines = [line.strip() for line in (lines_text or "").split("\n") if line.strip()]
    if not lines:
        return None, "Please enter at least one line of text."

    start_time = time.time()
    try:
        get_cached_conditionals(voice_audio, exaggeration=exaggeration)
        out_files = []
        os.makedirs("outputs", exist_ok=True)

        for idx, line in enumerate(lines, start=1):
            wav = MODEL.generate(line, temperature=temperature)
            save_path = f"outputs/batch_output_{idx:02d}_{int(time.time())}.wav"
            ta.save(save_path, wav, MODEL.sr)
            out_files.append(save_path)

        elapsed = time.time() - start_time
        msg = f"Generated {len(out_files)} audio files in {elapsed:.2f}s! Saved to 'outputs/' directory."
        # Return first audio for preview and message
        return out_files[0] if out_files else None, msg
    except Exception as e:
        return None, f"Error during batch generation: {str(e)}"


# Build Gradio UI
with gr.Blocks(title="Chatterbox AI Voice Generator") as demo:
    gr.Markdown(
        """
        # 🎙️ Chatterbox AI Voice Generator & Voice Cloner
        Synthesize high quality speech with **zero-shot voice cloning** powered by Chatterbox Turbo.
        """
    )

    with gr.Tabs():
        with gr.TabItem("Single Voice Generation"):
            with gr.Row():
                with gr.Column(scale=3):
                    text_input = gr.Textbox(
                        label="Text to Speak",
                        value="Hello! Welcome to our AI voice generator.",
                        lines=4,
                        placeholder="Type anything you want the voice to say...",
                    )
                    with gr.Accordion("⚙️ Voice & Tuning Options", open=False):
                        temperature_slider = gr.Slider(
                            minimum=0.1,
                            maximum=1.2,
                            value=0.8,
                            step=0.05,
                            label="Creativity / Temperature",
                            info="Lower is more deterministic; higher is more expressive.",
                        )
                        exaggeration_slider = gr.Slider(
                            minimum=0.0,
                            maximum=1.0,
                            value=0.0,
                            step=0.05,
                            label="Emotion Exaggeration",
                            info="Increases expressive emotional variance.",
                        )

                    generate_btn = gr.Button("🚀 Generate Speech", variant="primary", size="lg")

                with gr.Column(scale=2):
                    voice_upload = gr.Audio(
                        label="Voice Clone Reference (.wav or .mp3)",
                        type="filepath",
                        value="voice.wav" if DEFAULT_VOICE.exists() else None,
                    )
                    gr.Markdown("*(Leave blank or use the default voice to clone the built-in speaker)*")
                    audio_output = gr.Audio(label="Synthesized Audio Output", type="filepath")
                    status_text = gr.Markdown("")

            generate_btn.click(
                fn=generate_single_voice,
                inputs=[text_input, voice_upload, temperature_slider, exaggeration_slider],
                outputs=[audio_output, status_text],
            )

        with gr.TabItem("Batch Generation (Multiple Outputs)"):
            with gr.Row():
                with gr.Column(scale=3):
                    batch_text_input = gr.Textbox(
                        label="Enter Multiple Sentences (One per line)",
                        value="Line 1: Hello everyone!\nLine 2: Who the hell are you?\nLine 3: Have a wonderful day!",
                        lines=6,
                        placeholder="Each line will be generated as a separate audio file...",
                    )
                    batch_generate_btn = gr.Button("⚡ Generate All Lines", variant="primary", size="lg")

                with gr.Column(scale=2):
                    batch_voice_upload = gr.Audio(
                        label="Voice Clone Reference",
                        type="filepath",
                        value="voice.wav" if DEFAULT_VOICE.exists() else None,
                    )
                    batch_audio_output = gr.Audio(label="Latest Generated Preview", type="filepath")
                    batch_status_text = gr.Markdown("")

            batch_generate_btn.click(
                fn=generate_batch_voice,
                inputs=[batch_text_input, batch_voice_upload, temperature_slider, exaggeration_slider],
                outputs=[batch_audio_output, batch_status_text],
            )

    gr.Markdown(
        """
        ---
        💡 **Tip**: Audio prompts longer than 5 seconds with clear voice produce the cleanest voice cloning.
        """
    )

if __name__ == "__main__":
    # On Hugging Face Spaces, launch without inbrowser; the platform serves the UI
    demo.launch()
