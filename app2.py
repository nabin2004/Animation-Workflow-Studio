import gradio as gr
import subprocess
import tempfile
import os
import sys
import uuid
from pathlib import Path

def run_manim_code(code, history):
    """Execute Manim code and capture the output"""
    if not code.strip():
        return history + "\nPlease enter some Manim code to execute."
    
    # Initialize history
    if history:
        current_history = history + "\n\n"
    else:
        current_history = ""
    
    current_history += f"Executing Manim code:\n```python\n{code}\n```\n\n"
    
    # Create a temporary Python file with the Manim code
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        # Add necessary imports if not present
        if 'from manim import' not in code and 'import manim' not in code:
            full_code = "from manim import *\n\n" + code
        else:
            full_code = code
            
        f.write(full_code)
        temp_file = f.name
    
    try:
        # First, yield that we're starting execution
        yield current_history + "Starting Manim rendering...\n"
        
        # Run manim command
        output_dir = tempfile.mkdtemp()
        
        # Try to find scene classes in the code
        scene_classes = []
        for line in code.split('\n'):
            line = line.strip()
            if line.startswith('class ') and ('Scene)' in line or '(Scene' in line):
                class_name = line.split('class ')[1].split('(')[0].strip()
                scene_classes.append(class_name)
        
        # If no scene classes found, use -ql flag which will render all scenes
        if not scene_classes:
            cmd = [sys.executable, '-m', 'manim', '-ql', '--media_dir', output_dir, temp_file]
        else:
            # Render each scene class
            cmd = [sys.executable, '-m', 'manim', '-ql', '--media_dir', output_dir, temp_file] + scene_classes
        
        # Execute manim
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Capture output line by line
        full_output = current_history
        while True:
            output_line = process.stdout.readline()
            if output_line == '' and process.poll() is not None:
                break
            if output_line:
                full_output += output_line
                yield full_output
        
        # Get return code
        return_code = process.poll()
        
        if return_code == 0:
            full_output += "\n✅ Rendering completed successfully!\n"
        else:
            full_output += f"\n❌ Rendering failed with return code {return_code}\n"
        
        # Look for generated video files
        video_files = []
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                if file.endswith('.mp4'):
                    video_files.append(os.path.join(root, file))
        
        if video_files:
            full_output += f"\n🎥 Generated {len(video_files)} video file(s)\n"
        else:
            full_output += "\n⚠️ No video files generated\n"
        
        yield full_output
        
    except Exception as e:
        error_output = current_history + f"Error executing Manim code:\n{str(e)}\n"
        yield error_output
    finally:
        # Clean up temporary file
        try:
            os.unlink(temp_file)
        except:
            pass

def render_manim_with_video(code):
    """Execute Manim code and return both output and video files"""
    if not code.strip():
        return "Please enter some Manim code to execute.", None
    
    # Create a temporary Python file with the Manim code
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        # Add necessary imports if not present
        if 'from manim import' not in code and 'import manim' not in code:
            full_code = "from manim import *\n\n" + code
        else:
            full_code = code
            
        f.write(full_code)
        temp_file = f.name
    
    try:
        output_dir = tempfile.mkdtemp()
        output_text = "Starting Manim rendering...\n"
        
        # Try to find scene classes in the code
        scene_classes = []
        for line in code.split('\n'):
            line = line.strip()
            if line.startswith('class ') and ('Scene)' in line or '(Scene' in line):
                class_name = line.split('class ')[1].split('(')[0].strip()
                scene_classes.append(class_name)
        
        # Execute manim
        if not scene_classes:
            result = subprocess.run(
                [sys.executable, '-m', 'manim', '-ql', '--media_dir', output_dir, temp_file],
                capture_output=True, text=True
            )
        else:
            result = subprocess.run(
                [sys.executable, '-m', 'manim', '-ql', '--media_dir', output_dir, temp_file] + scene_classes,
                capture_output=True, text=True
            )
        
        output_text += result.stdout
        if result.stderr:
            output_text += "\nErrors:\n" + result.stderr
        
        # Look for the latest video file
        video_files = []
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                if file.endswith('.mp4'):
                    video_files.append(os.path.join(root, file))
        
        # Sort by modification time, get the most recent
        if video_files:
            video_files.sort(key=os.path.getmtime, reverse=True)
            video_path = video_files[0]
        else:
            video_path = None
        
        return output_text, video_path
        
    except Exception as e:
        return f"Error: {str(e)}", None
    finally:
        # Clean up temporary file
        try:
            os.unlink(temp_file)
        except:
            pass

# Create the Gradio interface
with gr.Blocks(title="Manim Code Runner") as demo:
    gr.Markdown("# 🎬 Manim Code Runner")
    gr.Markdown("Create mathematical animations using Manim. Write your code and see the output and generated videos!")
    
    with gr.Row():
        with gr.Column():
            code_input = gr.Textbox(
                label="Enter Manim Code",
                placeholder="""class CreateCircle(Scene):
    def construct(self):
        circle = Circle()
        self.play(Create(circle))
        self.wait()""",
                lines=12,
                max_lines=20
            )
            
            with gr.Row():
                run_live_button = gr.Button("Run Live Output", variant="primary")
                run_with_video_button = gr.Button("Run & Get Video", variant="secondary")
                clear_button = gr.Button("Clear All")
        
        with gr.Column():
            output_display = gr.Textbox(
                label="Execution Output",
                lines=12,
                max_lines=15,
                interactive=False,
                show_copy_button=True
            )
            video_output = gr.Video(
                label="Generated Animation",
                interactive=False
            )
    
    # Examples
    with gr.Accordion("📚 Manim Examples", open=False):
        gr.Examples(
            examples=[
                ["""class CreateCircle(Scene):
    def construct(self):
        circle = Circle()
        circle.set_fill(BLUE, opacity=0.5)
        self.play(Create(circle))
        self.wait()"""],
                
                ["""class SquareToCircle(Scene):
    def construct(self):
        circle = Circle()
        square = Square()
        square.flip(RIGHT)
        square.rotate(-3 * TAU / 8)
        circle.set_fill(PINK, opacity=0.5)

        self.play(Create(square))
        self.play(Transform(square, circle))
        self.play(FadeOut(square))"""],
                
                ["""class AnimatedEquation(Scene):
    def construct(self):
        equation = MathTex("\\\\frac{d}{dx}f(x)g(x)=", "f(x)\\\\frac{d}{dx}g(x)", "+", 
                          "g(x)\\\\frac{d}{dx}f(x)")
        self.play(Write(equation))
        self.wait()
        box1 = SurroundingRectangle(equation[1], color=BLUE)
        box2 = SurroundingRectangle(equation[3], color=YELLOW)
        self.play(Create(box1))
        self.wait()
        self.play(ReplacementTransform(box1, box2))
        self.wait()"""],
                
                ["""class MovingDot(Scene):
    def construct(self):
        dot = Dot(color=RED)
        self.play(dot.animate.shift(RIGHT * 3))
        self.play(dot.animate.shift(UP * 2))
        self.play(dot.animate.shift(LEFT * 3))
        self.play(dot.animate.shift(DOWN * 2))
        self.wait()"""]
            ],
            inputs=code_input,
            label="Click an example to load it"
        )
    
    # Event handlers
    run_live_button.click(
        fn=run_manim_code,
        inputs=[code_input, output_display],
        outputs=output_display,
        show_progress="minimal"
    )
    
    run_with_video_button.click(
        fn=render_manim_with_video,
        inputs=code_input,
        outputs=[output_display, video_output],
        show_progress="minimal"
    )
    
    clear_button.click(
        fn=lambda: ("", "", None),
        inputs=[],
        outputs=[code_input, output_display, video_output]
    )
    
    # Add some styling and instructions
    gr.Markdown("""
    ## 📖 How to Use:
    1. Write Manim code in the left panel (must contain a Scene class)
    2. Click **"Run Live Output"** to see execution logs in real-time
    3. Click **"Run & Get Video"** to generate and display the animation
    4. Use the examples to get started quickly!
    
    ## 💡 Tips:
    - Make sure your Scene class is named and contains a `construct(self)` method
    - Use `self.play()` for animations and `self.wait()` for pauses
    - The `-ql` flag renders in low quality for faster processing
    - Check the output console for any errors or warnings
    """)

if __name__ == "__main__":
    demo.launch(share=True)