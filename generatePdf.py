import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

# Get the list of all folders in the results directory
results_dir = "/home/kaju/Desktop/results/WithThresh"
folders = os.listdir(results_dir)

folders.sort()

# Create a new PDF canvas
# pdf = canvas.Canvas("results-withoutThresh.pdf", pagesize=A4)
pdf = canvas.Canvas("results-withThresh.pdf", pagesize=A4)
num_images_added = 0
# Iterate over the folders and generate a section for each one
for folder in folders:

    # Get the list of all images in the folder
    if(not os.path.exists(os.path.join(results_dir, folder, "plots"))): 
        continue
    images = os.listdir(os.path.join(results_dir, folder, "plots"))
    if(len(images) == 0):
        continue

    # Add a section header for the folder
    pdf.setFont("Helvetica", 16)
    pdf.drawString(100, 700, folder)

    # Iterate over the images and add them to the PDF
    img1, img2, img3, img4, img5, img6 = images
    pdf.drawImage(os.path.join(results_dir, folder, "plots", img1),50, 50, width=250, height=250)
    pdf.drawImage(os.path.join(results_dir, folder, "plots", img2),300, 50, width=250, height=250)
    pdf.drawImage(os.path.join(results_dir, folder, "plots", img3),50, 300, width=250, height=250)
    pdf.drawImage(os.path.join(results_dir, folder, "plots", img4),300, 300, width=250, height=250)
    pdf.showPage()
    pdf.drawImage(os.path.join(results_dir, folder, "plots", img5),50, 50, width=250, height=250)
    pdf.drawImage(os.path.join(results_dir, folder, "plots", img6),300, 50, width=250, height=250)
    pdf.showPage()


        # Move to the next page if necessary

# Save the PDF file
pdf.save()