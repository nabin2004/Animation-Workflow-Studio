# app.py
import gradio as gr
import requests

MCP_URL = "http://localhost:5000"

def query_stock(symbol):
    resp = requests.post(f"{MCP_URL}/tool/get_stock_price", json={"symbol": symbol})
    if resp.status_code == 200:
        return f"Current price of {symbol.upper()}: ${resp.json()['result']}"
    else:
        return f"Error: {resp.text}"

def show_portfolio(user_id):
    resp = requests.post(f"{MCP_URL}/tool/get_portfolio", json={"user_id": user_id})
    if resp.status_code == 200:
        portfolio = resp.json()["result"]
        output = ""
        total = 0
        for stock, info in portfolio.items():
            output += f"{stock}: {info['quantity']} shares @ ${info['current_price']} = ${info['total_value']}\n"
            total += info['total_value']
        output += f"\nPortfolio Total Value: ${round(total,2)}"
        return output
    else:
        return f"Error: {resp.text}"


with gr.Blocks() as demo:
    gr.Markdown("## Mini Stock MCP Demo")
    
    with gr.Tab("Stock Price"):
        stock_input = gr.Textbox(label="Stock Symbol")
        stock_btn = gr.Button("Get Price")
        stock_output = gr.Textbox(label="Price")
        stock_btn.click(query_stock, inputs=stock_input, outputs=stock_output)
    
    with gr.Tab("Portfolio"):
        user_input = gr.Textbox(label="User ID", value="demo")
        portfolio_btn = gr.Button("Show Portfolio")
        portfolio_output = gr.Textbox(label="Portfolio")
        portfolio_btn.click(show_portfolio, inputs=user_input, outputs=portfolio_output)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
