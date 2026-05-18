import os
import httpx    

import gradio as gr
from main import index  # מייבא את האינדקס המוכן
from workflow_chat import CyberShieldWorkflow, StatusEvent
async def chat_interface(message, history):
    # מעבירים את האינדקס ל-Workflow בזמן היצירה
    wf = CyberShieldWorkflow(index=index, timeout=60, verbose=True)
    handler = wf.run(query=message)
    
    status_display = ""
    async for event in handler.stream_events():
        if isinstance(event, StatusEvent):
            status_display = f"*{event.msg}*\n\n"
            yield status_display 
            
    final_result = await handler
    yield str(final_result)

with gr.Blocks(theme=gr.themes.Soft(primary_hue="blue")) as demo:
    gr.Markdown("# 🛡️ Cyber Shield - Live Workflow")
    gr.ChatInterface(fn=chat_interface)

if __name__ == "__main__":
    demo.launch()