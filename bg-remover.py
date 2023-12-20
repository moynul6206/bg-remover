import numpy as np
from tkinter import Tk, Label, Button, filedialog

def remove_background(image_path):
    # Load the image
    image = cv2.imread(image_path)
    
    # Create a mask initialized with zeros
    mask = np.zeros(image.shape[:2], np.uint8)
    
    # Define the background and foreground model
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)
    
    # Define the rectangle enclosing the foreground object
    rectangle = (50, 50, image.shape[1]-50, image.shape[0]-50)
    
    # Apply GrabCut algorithm to extract the foreground
    cv2.grabCut(image, mask, rectangle, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
    
    # Create a mask where the foreground and probable foreground are set to 1
    mask2 = np.where((mask==2) | (mask==0), 0, 1).astype('uint8')
    
    # Apply the mask to the original image
    result = image * mask2[:, :, np.newaxis]
    
    return result

def save_image(image):
    # Open the file dialog to save the edited image
    root = Tk()
    root.withdraw()
    save_path = filedialog.asksaveasfilename(defaultextension=".png")
    
    # Save the image to the specified path
    cv2.imwrite(save_path, image)
    
    # Show a success message
    Label(root, text="Image saved successfully!").pack()
    
    root.mainloop()

def upload_image():
    # Open a file dialog to select an image
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    
    # Remove the background
    result = remove_background(file_path)
    
    # Show a success message
    Label(root, text="Background removed successfully!").pack()
    
    # Display the result image
    cv2.imshow("Result", result)
    
    # Add a save button
    Button(root, text="Save", command=lambda: save_image(result)).pack()
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Create a GUI with an upload button
root = Tk()
root.title("Photo Background Remover")
Label(root, text="Click the button to upload an image").pack()
Button(root, text="Upload", command=upload_image).pack()

root.mainloop()
