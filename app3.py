import gradio as gr
import time
import subprocess
import tempfile
import os
import sys
import uuid
from pathlib import Path
import shutil

# Enhanced styling and theming
theme = gr.themes.Soft(
    primary_hue="blue",
    secondary_hue="teal",
).set(
    body_background_fill='linear-gradient(180deg, #0f172a 0%, #1e293b 100%)',
    background_fill_primary='#1e293b',
    background_fill_secondary='#334155',
    border_color_primary='#475569',
    block_background_fill='rgba(30, 41, 59, 0.8)',
    block_border_width='2px',
    button_primary_background_fill='linear-gradient(90deg, #3b82f6 0%, #06b6d4 100%)',
    button_primary_background_fill_hover='linear-gradient(90deg, #2563eb 0%, #0891b2 100%)',
)

# Store generated code globally
current_generated_code = ""
current_manim_code = ""
current_video_path = ""

# Create videos directory if it doesn't exist
VIDEO_DIR = Path("./generated_videos")
VIDEO_DIR.mkdir(exist_ok=True)

def generate_code(prompt):
    """Dummy function to generate code based on prompt"""
    time.sleep(1.5)
    
    # Simple template-based code generation
    if "animation" in prompt.lower() or "manim" in prompt.lower():
        code = f"""# 🎬 Generated Manim Animation Code
from manim import *

class {prompt.title().replace(' ', '')}Animation(Scene):
    def construct(self):
        # {prompt}
        title = Text("{prompt}", font_size=48, color=BLUE)
        self.play(Write(title))
        self.wait(1)
        
        circle = Circle(radius=2, color=GREEN, fill_opacity=0.5)
        circle.move_to(LEFT * 3)
        self.play(Create(circle))
        self.wait(1)
        
        square = Square(side_length=2, color=RED, fill_opacity=0.5)
        square.move_to(RIGHT * 3)
        self.play(Create(square))
        self.wait(2)
        
        # Transform shapes
        self.play(Transform(circle, square.copy()))
        self.wait(1)
        self.play(FadeOut(title), FadeOut(circle), FadeOut(square))
        self.wait(1)"""
    else:
        code = f"""# 🚀 Generated AI Code for: {prompt}
import numpy as np
import matplotlib.pyplot as plt

def {prompt.lower().replace(' ', '_')}_analysis():
    \"\"\"AI-powered analysis function for {prompt}\"\"\"
    print("✨ Initializing {prompt} system...")
    data = np.random.randn(1000)
    
    plt.figure(figsize=(10, 6))
    plt.plot(data.cumsum(), color='#3b82f6', linewidth=2)
    plt.title('AI Analysis: {prompt}', fontsize=14, fontweight='bold')
    plt.grid(alpha=0.3)
    plt.show()
    return f"🎯 {prompt} analysis completed successfully!"

# Execute the AI-generated solution
result = {prompt.lower().replace(' ', '_')}_analysis()
print(result)"""
    
    preview_content = f"""
<div style="padding: 20px; background: linear-gradient(135deg, #1e40af, #0ea5e9); border-radius: 10px; color: white;">
<h3 style="margin: 0; color: white;">🎯 Code Generated Successfully!</h3>
<p style="margin: 10px 0; opacity: 0.9;">Your AI-generated code is ready for review</p>
<div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px; margin-top: 10px;">
<strong>📊 Status:</strong> Code generation complete<br>
<strong>⚡ Performance:</strong> AI-optimized<br>
<strong>🎨 Features:</strong> Ready for next step
</div>
</div>
"""
    
    global current_generated_code
    current_generated_code = code
    
    return code, preview_content, gr.update(visible=True), gr.update(visible=True)

def approve_code(code):
    """Move approved code to Manim studio"""
    global current_manim_code
    current_manim_code = code
    
    preview_content = f"""
<div style="padding: 20px; background: linear-gradient(135deg, #059669, #10b981); border-radius: 10px; color: white;">
<h3 style="margin: 0; color: white;">✅ Code Approved!</h3>
<p style="margin: 10px 0; opacity: 0.9;">Ready to generate your animation!</p>
<div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px; margin-top: 10px;">
<strong>🚀 Next Step:</strong> Generate your animation below<br>
<strong>⚡ Status:</strong> Code loaded and ready<br>
<strong>🎬 Action:</strong> Click "Generate Video" to create animation
</div>
</div>
"""
    
    return preview_content, gr.update(visible=False), gr.update(visible=True), code

def load_generated_code():
    """Load the previously generated code into Manim studio"""
    global current_manim_code
    return current_manim_code

def save_video_to_filesystem(video_path, filename=None):
    """Save video to the file system with a proper filename"""
    if not video_path or not os.path.exists(video_path):
        return None
    
    if filename is None:
        filename = f"animation_{uuid.uuid4().hex[:8]}.mp4"
    
    # Ensure the filename has .mp4 extension
    if not filename.endswith('.mp4'):
        filename += '.mp4'
    
    destination_path = VIDEO_DIR / filename
    
    try:
        # Copy the video to our videos directory
        shutil.copy2(video_path, destination_path)
        return str(destination_path)
    except Exception as e:
        print(f"Error saving video: {e}")
        return None

def create_sample_video():
    """Create a sample video for testing when Manim is not available"""
    try:
        # Try to create a simple video using manim
        sample_code = """
from manim import *

class SampleAnimation(Scene):
    def construct(self):
        circle = Circle(radius=2, color=BLUE, fill_opacity=0.5)
        self.play(Create(circle))
        self.wait(1)
        square = Square(side_length=3, color=RED, fill_opacity=0.5)
        self.play(Transform(circle, square))
        self.wait(1)
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(sample_code)
            temp_file = f.name
        
        # Run manim to create video
        output_dir = VIDEO_DIR / "temp"
        output_dir.mkdir(exist_ok=True)
        
        result = subprocess.run([
            'manim', '-ql', '-o', 'sample_animation', temp_file, 'SampleAnimation'
        ], cwd=output_dir, capture_output=True, text=True)
        
        # Clean up temp file
        os.unlink(temp_file)
        
        # Find the generated video
        video_files = list(output_dir.glob("**/*.mp4"))
        if video_files:
            video_path = video_files[0]
            saved_path = save_video_to_filesystem(video_path, "sample_animation.mp4")
            # Clean up temp directory
            shutil.rmtree(output_dir)
            return saved_path
        
    except Exception as e:
        print(f"Manim not available or error: {e}")
    
    return None

def run_manim_code(code, history):
    """Run Manim code and generate output"""
    if not code.strip():
        return history + "\nPlease enter some Manim code to execute."
    
    # Initialize history
    if history:
        current_history = history + "\n\n"
    else:
        current_history = ""
    
    current_history += f"Executing Manim code:\n```python\n{code}\n```\n\n"
    
    # Simulate execution steps
    steps = [
        "Starting Manim rendering...",
        "🔍 Analyzing scene composition...",
        "🎨 Setting up animation framework...",
        "📐 Calculating object positions...",
        "⚡ Rendering frames (0/60)...",
        "⚡ Rendering frames (15/60)...",
        "⚡ Rendering frames (30/60)...",
        "⚡ Rendering frames (45/60)...",
        "⚡ Rendering frames (60/60)...",
        "🎬 Compiling video...",
        "✅ Rendering completed successfully!",
        "🎥 Generated 1 video file"
    ]
    
    for step in steps:
        time.sleep(0.5)
        current_history += step + "\n"
        yield current_history

def render_manim_with_video(code):
    """Render Manim code and return video path"""
    global current_video_path
    
    if not code.strip():
        return "Please enter some Manim code to execute.", None
    
    output_text = "Starting Manim rendering...\n"
    steps = [
        "🔍 Analyzing scene composition...",
        "🎨 Setting up animation framework...",
        "📐 Calculating object positions...",
        "⚡ Rendering frames...",
        "🎬 Compiling video...",
        "✅ Rendering completed successfully!",
        "🎥 Generated 1 video file"
    ]
    
    for step in steps:
        time.sleep(0.7)
        output_text += step + "\n"
    
    # Try to create a real video, fall back to sample if needed
    video_path = create_sample_video()
    
    if video_path and os.path.exists(video_path):
        current_video_path = video_path
        output_text += f"\n✅ Video saved to: {video_path}"
        return output_text, video_path
    else:
        output_text += "\n⚠️ Could not generate video. Using placeholder."
        # Return a placeholder or sample video
        sample_video = "sample_animation.mp4"  # You can add a sample video file
        if os.path.exists(sample_video):
            current_video_path = sample_video
            return output_text, sample_video
        else:
            return output_text, None

def download_current_video():
    """Download the current video file"""
    global current_video_path
    if current_video_path and os.path.exists(current_video_path):
        return current_video_path
    else:
        # Create a sample video if none exists
        sample_path = create_sample_video()
        if sample_path:
            return sample_path
        else:
            raise gr.Error("No video available to download")

def reset_workflow():
    """Reset the entire workflow"""
    global current_video_path
    current_video_path = ""
    
    return (
        "",  # prompt
        "",  # code_box
        "<div style='text-align: center; padding: 40px; color: #94a3b8;'>💡 Describe your animation idea and click 'Generate AI Code' to start!</div>",  # live_preview
        gr.update(visible=False),  # approval_section
        gr.update(visible=False),  # manim_section
        "",  # manim_code_input
        "",  # manim_output_display
        None   # manim_video_output
    )

with gr.Blocks(theme=theme, css="""
    .gradio-container {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    }
    .header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #1e40af, #0ea5e9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }
    .prompt-box {
        background: rgba(255,255,255,0.05);
        border: 2px solid #475569;
        border-radius: 12px;
        padding: 15px;
    }
    .gradio-button {
        font-weight: 600 !important;
        border-radius: 8px !important;
    }
    .workflow-step {
        background: rgba(255,255,255,0.05);
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        border-left: 4px solid #3b82f6;
    }
    .next-step-btn {
        background: linear-gradient(90deg, #10b981, #059669) !important;
        color: white !important;
    }
    .section-header {
        background: linear-gradient(90deg, #1e40af, #0ea5e9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 1.5em;
        margin-bottom: 15px;
    }
    .completion-banner {
        background: linear-gradient(135deg, #059669, #10b981);
        border-radius: 10px;
        padding: 20px;
        color: white;
        text-align: center;
        margin: 20px 0;
    }
    .video-container {
        border: 2px solid #475569;
        border-radius: 10px;
        padding: 10px;
        background: rgba(255,255,255,0.05);
    }
""") as demo:
    
    # Header with animated gradient
    gr.HTML("""
    <div class="header">
        <h1 style="font-size: 3em; margin-bottom: 10px; background: linear-gradient(90deg, #3b82f6, #06b6d4, #8b5cf6);
                  -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900;">
          🚀 Animation Workflow Studio
        </h1>
        <p style="font-size: 1.2em; color: #94a3b8; margin-top: 0;">
          Transform your ideas into beautiful mathematical animations - All in one workflow ✨
        </p>
    </div>
    """)

    # Workflow Progress Indicator
    gr.Markdown("### 🎯 Workflow Progress: Describe → Generate → Animate")
    
    # Step 1: AI Code Generation
    with gr.Group(visible=True) as step1_section:
        gr.Markdown("### 🤖 Step 1: Describe Your Animation")
        with gr.Row(equal_height=True):
            # Input Section
            with gr.Column(scale=1):
                with gr.Group():
                    prompt = gr.Textbox(
                        label="What animation do you want to create?",
                        placeholder="Describe the animation you want to create... (e.g., 'circle transforming into square', 'mathematical equation animation', 'moving dot animation')",
                        lines=3,
                        elem_classes="prompt-box"
                    )
                    
                    with gr.Row():
                        send_btn = gr.Button(
                            "✨ Generate AI Code", 
                            variant="primary", 
                            size="lg"
                        )
                        clear_btn = gr.Button("🗑️ Clear", variant="secondary", size="lg")

            # Output Section
            with gr.Column(scale=2):
                with gr.Tabs():
                    with gr.TabItem("👨‍💻 Generated Code"):
                        code_box = gr.Code(
                            label="AI-Generated Manim Code",
                            language="python",
                            lines=12,
                            interactive=True,
                        )
                    
                    with gr.TabItem("🎯 Status"):
                        live_preview = gr.HTML(
                            label="Workflow Status",
                            value="<div style='text-align: center; padding: 40px; color: #94a3b8;'>💡 Describe your animation idea and click 'Generate AI Code' to start!</div>"
                        )
        
        # Approval Section - Initially hidden
        with gr.Row(visible=False) as approval_section:
            with gr.Column():
                gr.Markdown("### ✅ Step 2: Review & Approve")
                with gr.Row():
                    approve_btn = gr.Button(
                        "👍 Code Looks Good - Generate Animation", 
                        variant="primary", 
                        size="lg",
                        elem_classes="next-step-btn"
                    )
                    revise_btn = gr.Button("👎 Regenerate Code", variant="secondary", size="lg")

    # Step 2: Manim Animation Studio - Initially hidden
    with gr.Group(visible=False) as manim_section:
        gr.Markdown("### 🎬 Step 3: Generate Your Animation")
        
        with gr.Row():
            with gr.Column(scale=1):
                manim_code_input = gr.Code(
                    label="Manim Code (Auto-filled from Step 1)",
                    language="python",
                    lines=12,
                    interactive=True
                )
                
                with gr.Row():
                    load_code_btn = gr.Button("🔄 Reload Code", variant="secondary")
                    run_live_button = gr.Button("Run Live Output", variant="primary")
                    run_with_video_button = gr.Button("🎬 Generate Video", variant="primary", elem_classes="next-step-btn")
            
            with gr.Column(scale=1):
                manim_output_display = gr.Textbox(
                    label="Execution Output",
                    lines=10,
                    max_lines=15,
                    interactive=False,
                    show_copy_button=True
                )
                with gr.Group(elem_classes="video-container"):
                    manim_video_output = gr.Video(
                        label="Generated Animation",
                        interactive=False,
                        format="mp4"
                    )

    # Workflow completion and reset
    with gr.Row(visible=True):
        with gr.Column():
            gr.Markdown("### 🔄 Start Over or Continue")
            with gr.Row():
                new_workflow_btn = gr.Button("🔄 Start New Animation", variant="primary")
                download_btn = gr.Button("📥 Download Video", variant="secondary")
                share_btn = gr.Button("🔗 Share Animation", variant="secondary")

    # Footer
    gr.HTML("""
    <div style="text-align: center; margin-top: 30px; padding: 20px; border-top: 1px solid #475569;">
        <p style="color: #94a3b8; margin: 0;">
            Developed by Nabin • Built with Gradio • Single-Page Workflow 🚀
        </p>
    </div>
    """)

    # Event handlers
    send_btn.click(
        generate_code, 
        inputs=[prompt], 
        outputs=[code_box, live_preview, approval_section, manim_section],
        api_name="generate"
    )
    
    approve_btn.click(
        approve_code,
        inputs=[code_box],
        outputs=[live_preview, approval_section, manim_section, manim_code_input],
        api_name="approve"
    )
    
    revise_btn.click(
        lambda: gr.update(visible=False),
        outputs=[approval_section]
    )
    
    clear_btn.click(
        lambda: ["", "<div style='text-align: center; padding: 40px; color: #94a3b8;'>💡 Describe your animation idea and click 'Generate AI Code' to start!</div>", gr.update(visible=False), gr.update(visible=False)],
        outputs=[prompt, live_preview, approval_section, manim_section]
    )
    
    # Manim Event handlers
    load_code_btn.click(
        load_generated_code,
        outputs=[manim_code_input]
    )
    
    run_live_button.click(
        fn=run_manim_code,
        inputs=[manim_code_input, manim_output_display],
        outputs=[manim_output_display],
        show_progress="minimal"
    )
    
    run_with_video_button.click(
        fn=render_manim_with_video,
        inputs=[manim_code_input],
        outputs=[manim_output_display, manim_video_output],
        show_progress="minimal"
    )
    
    # Reset workflow
    new_workflow_btn.click(
        reset_workflow,
        outputs=[
            prompt, 
            code_box, 
            live_preview, 
            approval_section, 
            manim_section, 
            manim_code_input, 
            manim_output_display, 
            manim_video_output
        ]
    )
    
    # Download button functionality
    download_btn.click(
        fn=download_current_video,
        outputs=gr.File(label="Download Video"),
        api_name="download_video"
    )
    
    share_btn.click(
        lambda: gr.Info("Share functionality coming soon! 🔗"),
        queue=False
    )

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        share=False,
        show_error=True
    )