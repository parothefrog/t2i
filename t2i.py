from PIL import Image, ImageDraw, ImageFont
import argparse
parser = argparse.ArgumentParser(
    prog="Transcript 2 Image",
    description="Python Script to turn chat transcripts (Copy + Paste) into images that look fancy",
    epilog="Have fun, and don't leak too much secrets"
)
parser.add_argument("ACC1", help="Display name of the first user present in the transcript",
                    type=str,
                    default='NULL')
parser.add_argument("ACC1A", help="Alignment of their chat bubbles (only 'left' or 'right' accepted)",
                    type=str,
                    choices=("left", "right"))
parser.add_argument("ACC2",help="Display name of the second user present in the transcript",
                    type=str,
                    default='NULL')
parser.add_argument("ACC2A", help="Alignment of their chat bubbles (only 'left' or 'right' accepted)",
                    type=str,
                    choices=("left", "right"))
parser.add_argument("input_file", help="Your transcript file",
                    type=str)
args = parser.parse_args()

ACC1 = args.ACC1
ACC1A = args.ACC1A
ACC2 = args.ACC2
ACC2A = args.ACC2A
input_file = args.input_file


print(r"""
          /$$$$$$$$ /$$$$$$  /$$$$$$          
         |__  $$__//$$__  $$|_  $$_/          
 /$$$$ /$$$$| $$  |__/  \ $$  | $$ /$$$$ /$$$$
|____/|____/| $$    /$$$$$$/  | $$|____/|____/
 /$$$$ /$$$$| $$   /$$____/   | $$ /$$$$ /$$$$
|____/|____/| $$  | $$        | $$|____/|____/
            | $$  | $$$$$$$$ /$$$$$$          
            |__/  |________/|______/          
                 v1.0 by PARO                                         
                                              """)
print('Making a picture of your transcript, with the following values:')
print('Account 1: ', ACC1)
print('Align: ', ACC1A)
print('Account 2: ', ACC2)
print('Align: ', ACC2A)
print('Transcript File: ', input_file)

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
        if ACC1 in line:
            if temp_message:
                message_lines = wrap_text(' '.join(temp_message), regular_font, max_bubble_width - 2*extra_bubble_padding)
                wrapped_content.append((message_lines, message_color, alignment, sender_name))
                temp_message = []
            sender_name = line
            message_color = 'lightgray'
            alignment = ACC1A
        elif ACC2 in line:
            if temp_message:
                message_lines = wrap_text(' '.join(temp_message), regular_font, max_bubble_width - 2*extra_bubble_padding)
                wrapped_content.append((message_lines, message_color, alignment, sender_name))
                temp_message = []
            sender_name = line
            message_color = 'lightgray'
            alignment = ACC2A
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

    image.save('chat_transcript.png')

# Read the transcript from the file and call the function
with open(args.input_file, 'r') as f:
    transcript = f.read()
    generate_chat_image(transcript)

print("")
print('Output file "chat_transcript.png" generated. Enjoy!')
