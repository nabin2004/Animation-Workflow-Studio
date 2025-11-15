import gradio as gr
import time

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
    # block_border_radius='lg',  
    button_primary_background_fill='linear-gradient(90deg, #3b82f6 0%, #06b6d4 100%)',
    button_primary_background_fill_hover='linear-gradient(90deg, #2563eb 0%, #0891b2 100%)',
)

def generate_code(prompt):
    # Simulate AI processing time
    time.sleep(1.5)
    
    # Enhanced code generation with different templates
    code_templates = [
        f"""# 🚀 Generated AI Code for: {prompt}
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
print(result)""",

        f"""# ⚡ AI Solution: {prompt}
class {prompt.title().replace(' ', '')}Processor:
    def __init__(self):
        self.model_loaded = True
        self.optimized = True
    
    def process(self, input_data):
        \"\"\"AI processing pipeline for {prompt}\"\"\"
        print(f\"🤖 Processing {{input_data}} using {prompt} AI...\")
        return f\"AI processed: {{input_data}} with {prompt} optimization\"
    
    def deploy(self):
        \"\"\"Deploy the AI solution\"\"\"
        return \"🚀 Deployment successful! System ready for {prompt}\"

# Initialize and run AI system
processor = {prompt.title().replace(' ', '')}Processor()
print(processor.deploy())"""
    ]
    
    import random
    code = random.choice(code_templates)
    
    preview_content = f"""
<div style="padding: 20px; background: linear-gradient(135deg, #1e40af, #0ea5e9); border-radius: 10px; color: white;">
<h3 style="margin: 0; color: white;">🎯 Live Preview: {prompt}</h3>
<p style="margin: 10px 0; opacity: 0.9;">AI is generating optimized code for your request...</p>
<div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px; margin-top: 10px;">
<strong>📊 Status:</strong> Code generation complete<br>
<strong>⚡ Performance:</strong> AI-optimized<br>
<strong>🎨 Features:</strong> Ready for deployment
</div>
</div>
"""
    return code, preview_content

def customize_and_compile(code):
    # Simulate compilation process
    time.sleep(2)
    
    # Enhanced compilation with status updates
    compiled_code = code + f"""
    
# 🔧 AI Compilation Report
print("\\n" + "="*50)
print("🤖 AI COMPILATION SUCCESSFUL")
print("="*50)
print("✅ All dependencies resolved")
print("✅ Code optimized for performance")
print("✅ Security checks passed")
print("✅ Ready for production deployment")
print("="*50)
"""
    
    preview_content = f"""
<div style="padding: 20px; background: linear-gradient(135deg, #059669, #10b981); border-radius: 10px; color: white;">
<h3 style="margin: 0; color: white;">✅ Compilation Successful!</h3>
<p style="margin: 10px 0; opacity: 0.9;">Your AI-generated code is ready to run</p>
<div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px; margin-top: 10px;">
<strong>📦 Build:</strong> Production-ready<br>
<strong>⚡ Performance:</strong> Optimized<br>
<strong>🔒 Security:</strong> All checks passed<br>
<strong>🚀 Status:</strong> Ready for deployment
</div>
</div>
"""
    return compiled_code, preview_content

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
""") as demo:
    
    # Header with animated gradient
    gr.HTML("""
    <div class="header">
        <h1 style="font-size: 3em; margin-bottom: 10px; background: linear-gradient(90deg, #3b82f6, #06b6d4, #8b5cf6);
                  -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900;">
          🚀 Code Producer
        </h1>
        <p style="font-size: 1.2em; color: #94a3b8; margin-top: 0;">
          Transform your ideas into production-ready code with AI magic ✨
        </p>
    </div>
    """)

    with gr.Row(equal_height=True):
        # Input Section
        with gr.Column(scale=1):
            with gr.Group():
                gr.Markdown("### 💡 Your Idea")
                prompt = gr.Textbox(
                    label="",
                    placeholder="Describe what you want to build... (e.g., 'data analysis dashboard', 'neural network', 'web scraper')",
                    lines=3,
                    elem_classes="prompt-box"
                )
                
                with gr.Row():
                    send_btn = gr.Button(
                        "✨ Generate AI Code", 
                        variant="primary", 
                        size="lg",
                        scale=2
                    )
                    clear_btn = gr.Button("🗑️ Clear", variant="secondary", size="lg", scale=1)

        # Output Section
        with gr.Column(scale=2):
            with gr.Tabs():
                with gr.TabItem("👨‍💻 Generated Code"):
                    code_box = gr.Code(
                        label="AI-Generated Code",
                        language="python",
                        lines=15,
                        interactive=True,
                        # show_copy_button=True
                    )
                
                with gr.TabItem("🎯 Live Preview"):
                    live_preview = gr.HTML(
                        label="Real-time Preview",
                        value="<div style='text-align: center; padding: 40px; color: #94a3b8;'>💡 Enter your idea and click 'Generate AI Code' to see the magic happen!</div>"
                    )

    # Action Buttons Row
    with gr.Row():
        compile_btn = gr.Button(
            "⚡ Customize & Compile", 
            variant="primary", 
            size="lg"
        )
        export_btn = gr.Button("📤 Export Project", variant="secondary", size="lg")
        share_btn = gr.Button("🔗 Share", variant="secondary", size="lg")

    # Footer
    gr.HTML("""
    <div style="text-align: center; margin-top: 30px; padding: 20px; border-top: 1px solid #475569;">
        <p style="color: #94a3b8; margin: 0;">
            Developed by Nabin • Built with Gradio • Ready for Production 🚀
        </p>
    </div>
    """)

    # Event handlers
    send_btn.click(
        generate_code, 
        inputs=prompt, 
        outputs=[code_box, live_preview],
        api_name="generate"
    )
    
    compile_btn.click(
        customize_and_compile, 
        inputs=code_box, 
        outputs=[code_box, live_preview],
        api_name="compile"
    )
    
    clear_btn.click(
        lambda: ["", "<div style='text-align: center; padding: 40px; color: #94a3b8;'>💡 Enter your idea and click 'Generate AI Code' to see the magic happen!</div>"],
        outputs=[prompt, live_preview]
    )
    
    # Placeholder buttons
    export_btn.click(
        lambda: gr.Info("Export feature coming soon! 🚀"),
        queue=False
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