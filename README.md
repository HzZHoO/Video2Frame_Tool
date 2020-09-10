# Video2Frame_Tool
<div align=center>![icon](/128.ico)  
Simple tool to extract frames from videos.   
It has UI (user interface) and can convert all videos under a selected directory which must have **pure English path**.  
The UI is designed for Chinese users, but I think it's easy to convert it to English version.  
  
**Note**:  
For a video with path `parent_dir/0000.mp4`, the frames of it will be write to directory `parent_dir/0000`
  
## 1.Run the tool!
```bash
python Video2Frames.py
```  

## 2.Select a directory containing videos
<div align=center>![select_dir](/ui_captures/select_dir.PNG)

## 3.Input frame extraction step
Input an integer (between 1 and 1000) as the step for frame extraction.  
By default, the step is 1.  
<div align=center>![input_step](/ui_captures/input_step.PNG)

## 4.Start the conversion!
<div align=center>![start_conversion](/ui_captures/start_conversion.PNG)
