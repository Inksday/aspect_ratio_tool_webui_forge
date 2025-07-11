# Aspect Ratio Tool for SD Web UI Forge

![aspectratiotool](https://github.com/user-attachments/assets/b5a74660-cb8c-4c35-a63e-5f1c876e4758)

This Gradio 4 extension enhances the txt2img and img2img tabs in Stable Diffusion WebUI Forge by providing tools to calculate and adjust image dimensions based on aspect ratios and scaling factors.

## Features

- **Aspect Ratio Calculation**: Input a desired height, select an aspect ratio, and calculate the corresponding width.

- **Preset Aspect Ratios**: Choose from popular aspect ratios like 16:9, 4:3, 1:1, and more.

- **Copy Height**: Quickly copy the current height from the txt2img or img2img tabs.

- **Lock Width to 16px Increments**: Ensure the calculated width is a multiple of 16 pixels for compatibility with certain models.

- **Scaling**: Apply a scaling factor to both width and height based on an input number.

## Installation

1. Navigate to the `Extensions` tab in Stable Diffusion WebUI Forge.

2. Click on `Install from URL`.

3. Paste the following URL into the input field:

```plaintext
https://github.com/Inksday/aspect_ratio_tool_webui_forge
```

4. Click `Install`.

5. After installation, click `Apply and Restart UI`.

## Usage

- **Aspect Ratio Calculation**: Enter a height value, select an aspect ratio, and click `Calculate Width` to determine the corresponding width.

- **Change height to nearest multiple of 16**: If your height is not a multiple of 16 and you wish it to be. Press the *16 button.

- **Preset Aspect Ratios**: Click on a preset aspect ratio button to automatically set the aspect ratio.

- **Copy Height**: Click `Copy Height` to copy the current height from the txt2img or img2img tabs.

- **Lock Width to 16px Increments**: Check the `Lock Width to 16px` checkbox to ensure the calculated width is a multiple of 16 pixels.

- **Scaling**: Enter a scaling factor and click `Apply Scaling` to adjust both width and height accordingly.

## License

This extension is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
