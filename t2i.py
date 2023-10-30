from PIL import Image, ImageDraw, ImageFont

def wrap_text(text, font, max_width):
    """Wrap the provided text within the specified width."""
    lines = []
    words = text.split()
    while words:
        line = ''
        while words and font.getlength(line + words[0]) <= max_width:
            line += (words.pop(0) + ' ')
        lines.append(line)
    return lines

def generate_chat_image(transcript):
    transcript_lines = transcript.split('\n')
    
    regular_font = ImageFont.truetype("./arial.ttf", 14)
    bold_font = ImageFont.truetype("./arial_bold.ttf", 14)
    
    padding = 10
    bubble_spacing = 5
    extra_bubble_padding = 5
    total_image_width = 650
    max_bubble_width = int(2/3 * total_image_width)
    line_height = regular_font.getbbox("A")[3]
    
    wrapped_content = []
    temp_message = []
    sender_name = None
    message_color = None
    alignment = None
    
    for line in transcript_lines:
        if "COMPROMISED ACCOUNT" in line:
            if temp_message:
                message_lines = wrap_text(' '.join(temp_message), regular_font, max_bubble_width - 2*extra_bubble_padding)
                wrapped_content.append((message_lines, message_color, alignment, sender_name))
                temp_message = []
            sender_name = line
            message_color = 'lightgray'
            alignment = 'left'
        elif "PARO" in line:
            if temp_message:
                message_lines = wrap_text(' '.join(temp_message), regular_font, max_bubble_width - 2*extra_bubble_padding)
                wrapped_content.append((message_lines, message_color, alignment, sender_name))
                temp_message = []
            sender_name = line
            message_color = 'lightgray'
            alignment = 'right'
        else:
            temp_message.append(line)
            
    if temp_message:
        message_lines = wrap_text(' '.join(temp_message), regular_font, max_bubble_width - 2*extra_bubble_padding)
        wrapped_content.append((message_lines, message_color, alignment, sender_name))

    total_lines = sum([len(item[0]) for item in wrapped_content]) + len(wrapped_content)
    height = (total_lines * (line_height + padding)) + bubble_spacing * len(wrapped_content)
    
    image = Image.new('RGBA', (total_image_width, int(height) + 500), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    y_position = padding

    for lines, color, align, sender in wrapped_content:
        title_position = (padding, y_position) if align == 'left' else (total_image_width - bold_font.getlength(sender) - padding, y_position)
        
        draw.text(title_position, sender, font=bold_font, fill='black')
        y_position += line_height + padding
        
        text_widths = [regular_font.getlength(line) for line in lines]
        max_text_width = max(text_widths) if text_widths else 0
        bubble_width = max_text_width + 2*extra_bubble_padding
        
        bubble_height = len(lines) * (line_height + padding) + 2 * extra_bubble_padding
        text_start = y_position + extra_bubble_padding

        if align == 'left':
            draw.rectangle([padding, y_position, padding + bubble_width, y_position + bubble_height], fill=color, outline='black')
        else:
            draw.rectangle([total_image_width - bubble_width - padding, y_position, total_image_width - padding, y_position + bubble_height], fill=color, outline='black')

        for line in lines:
            line_width = regular_font.getlength(line)
            text_position = (padding + extra_bubble_padding, text_start)
            
            if align == 'right':
                text_position = (total_image_width - line_width - padding - extra_bubble_padding, text_start)
            
            draw.text(text_position, line, font=regular_font, fill='black')
            
            text_start += line_height + padding

        y_position += bubble_height + bubble_spacing

    image.save('chat_image_with_titles.png')

# Read the transcript from the file and call the function
with open('transcript.txt', 'r') as f:
    transcript = f.read()
    generate_chat_image(transcript)
