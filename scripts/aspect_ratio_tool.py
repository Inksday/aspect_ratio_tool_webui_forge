import gradio as gr
from modules import scripts

class AspectRatioTool(scripts.Script):
    def title(self):
        return "Aspect Ratio Tool"

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def build_ui(self, suffix=""):
        with gr.Accordion(open=False, label=self.title(), elem_id=f"aspect-ratio-tool{suffix}"):
            with gr.Row():
                copy_txt2img_btn = gr.Button(value="⬇ Copy from txt2img height", elem_id=f"copy_txt2img_btn{suffix}")
                copy_img2img_btn = gr.Button(value="⬇ Copy from img2img height", elem_id=f"copy_img2img_btn{suffix}")
                round_height_btn = gr.Button(value="*16", elem_id=f"round_height_btn{suffix}")

            with gr.Row():
                height_input = gr.Number(label="Height (pixels)", value=512, precision=0, minimum=1, step=1,
                                         elem_id=f"ar_height{suffix}")

            with gr.Row():
                aspect_ratio_input = gr.Textbox(label="Aspect Ratio (e.g., 16:9 or 1.78)", value="16:9",
                                                elem_id=f"ar_aspect{suffix}")

            with gr.Row():
                width_output_display = gr.Number(label="Calculated Width (pixels)", interactive=False, precision=0,
                                                 elem_id=f"ar_width_disp{suffix}")
                lock_width_checkbox = gr.Checkbox(label="Lock Width to Nearest Multiple of 16", value=True,
                                                  elem_id=f"ar_lock{suffix}")

            width_output_hidden = gr.Textbox(visible=False, elem_id=f"ar_width_hidden{suffix}")

            with gr.Row():
                presets = ["1:1", "3:2", "4:3", "16:9", "21:9", "32:9", "2:3", "3:4", "9:16", "9:21", "9:32"]
                preset_buttons = {r: gr.Button(value=r, elem_id=f"preset_{r.replace(':','_')}{suffix}") for r in presets}

            calculate_button = gr.Button(value="Calculate Width", elem_id=f"ar_calculate_button{suffix}")

            with gr.Row():
                scale_factor_input = gr.Number(label="Scale Factor", value=2.0, precision=2, minimum=0.01, step=0.01,
                                               elem_id=f"ar_scale_factor{suffix}")
                scale_btn = gr.Button(value="Scale", elem_id=f"ar_scale_btn{suffix}")

            with gr.Row():
                scaled_height_output = gr.Number(label="Scaled Height (pixels)", interactive=False, precision=0,
                                                 elem_id=f"ar_scaled_height{suffix}")
                scaled_width_output = gr.Number(label="Scaled Width (pixels)", interactive=False, precision=0,
                                                elem_id=f"ar_scaled_width{suffix}")

            def calculate_width(height, aspect_ratio, lock_width):
                try:
                    if ":" in aspect_ratio:
                        w_str, h_str = aspect_ratio.split(":")
                        ratio = float(w_str) / float(h_str)
                    else:
                        ratio = float(aspect_ratio)
                    width = int(round(height * ratio))
                    if lock_width:
                        width = int(round(width / 16) * 16)
                    return width, str(width)
                except:
                    return 0, "0"

            def round_height_to_16(height):
                if isinstance(height, (int, float)):
                    return int(round(height / 16) * 16)
                return height

            def set_aspect_ratio(ratio):
                return ratio

            def scale_size(height, width_str, scale_factor):
                try:
                    w = int(width_str)
                    s = float(scale_factor)
                    return max(1, int(round(height * s))), max(1, int(round(w * s)))
                except:
                    return None, None

            for r, btn in preset_buttons.items():
                btn.click(fn=lambda r=r: set_aspect_ratio(r), outputs=aspect_ratio_input)

            round_height_btn.click(fn=round_height_to_16, inputs=height_input, outputs=height_input)

            calculate_button.click(
                fn=calculate_width,
                inputs=[height_input, aspect_ratio_input, lock_width_checkbox],
                outputs=[width_output_display, width_output_hidden]
            )

            scale_btn.click(
                fn=scale_size,
                inputs=[height_input, width_output_hidden, scale_factor_input],
                outputs=[scaled_height_output, scaled_width_output]
            )

            copy_txt2img_btn.click(
                fn=None, inputs=[], outputs=[], _js=f"""
                () => {{
                    const src = document.querySelector('#txt2img_height input');
                    const tgt = document.querySelector('#ar_height{suffix} input');
                    if (src && tgt) {{
                        tgt.value = src.value;
                        tgt.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        tgt.dispatchEvent(new Event('change', {{ bubbles: true }}));
                        setTimeout(() => document.querySelector('#ar_calculate_button{suffix}')?.click(), 50);
                    }}
                }}
                """
            )

            copy_img2img_btn.click(
                fn=None, inputs=[], outputs=[], _js=f"""
                () => {{
                    const src = document.querySelector('#img2img_height input');
                    const tgt = document.querySelector('#ar_height{suffix} input');
                    if (src && tgt) {{
                        tgt.value = src.value;
                        tgt.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        tgt.dispatchEvent(new Event('change', {{ bubbles: true }}));
                        setTimeout(() => document.querySelector('#ar_calculate_button{suffix}')?.click(), 50);
                    }}
                }}
                """
            )

            return [
                height_input, aspect_ratio_input,
                width_output_display, width_output_hidden,
                scale_factor_input, scaled_height_output,
                scaled_width_output, round_height_btn,
                copy_txt2img_btn, copy_img2img_btn,
                *preset_buttons.values()
            ]

    def ui(self, is_img2img):
        suffix = "_img2img" if is_img2img else ""
        tab = "img2img" if is_img2img else "txt2img"
        with gr.Tab(tab):
            return self.build_ui(suffix)

    def process_before_every_sampling(self, p, height, aspect_ratio, width, *args, **kwargs):
        try:
            if isinstance(width, (int, float)) and width > 0 and isinstance(height, (int, float)) and height > 0:
                p.width = int(width)
                p.height = int(height)
        except Exception as e:
            print(f"[AspectRatioTool] Error setting width/height: {e}")
