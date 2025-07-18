# plant_disease_model.py
import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image
IMG_SIZE = 128
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
DIAGNOSIS = {
    "mango_Anthracnose":"Dark, sunken lesions appear on leaves, stems, or fruits, often leading to tissue death and premature leaf drop",
    "mango_Die Back":"Progressive death of twigs, branches, or shoots starting at the tips, commonly seen in woody plants",
    "mango_Healthy": "The plant appears healthy with no visible signs of disease.",
    "mango_Sooty Mould":"Black, powdery fungal growth coats leaves or fruit surfaces, usually growing on honeydew from sap-sucking insects",
    "mango_Gall Midge":"Presence of small maggots or orange larvae inside swollen, discolored stem bases, often causing plant injury at field edges",
    "mango_Cutting Weevil":"Feeding damage by larvae or adults leads to notched, ragged leaves and potential injury to young plant cuttings",
    "mango_Powdery Mildew": "Fungal infection appearing as orange-red pustules on the underside of leaves.", 
    "mango_Bacterial Canker":"Feeding damage by larvae or adults leads to notched, ragged leaves and potential injury to young plant cuttings"
}
TREATMENTS = {
    "mango_Anthracnose": "Spray fungicides like Mancozeb or Copper oxychloride. Remove infected debris and avoid overhead irrigation.",
    "mango_Die Back":"Prune and burn affected branches. Use copper oxychloride spray and ensure proper drainage.",
    "mango_Healthy": "No treatment needed. Maintain good plant health with proper watering, sunlight, and nutrients.",
    "mango_Sooty Mould": "Wash leaves with mild soap solution. Control aphids and whiteflies. Use horticultural oil sprays.",
    "mango_Gall Midge": "Remove and destroy infested parts. Use neem-based insecticides and maintain field hygiene.",
    "mango_Cutting Weevil": "Destroy infested cuttings. Apply systemic insecticides and practice crop rotation.",
    "mango_Powdery Mildew": "Apply sulfur-based or neem oil sprays. Ensure good air circulation and avoid overhead watering.",
    "mango_Bacterial Canker": "Prune infected branches, disinfect pruning tools, and apply copper-based bactericides.",
}

class CNNModel(nn.Module):
    def __init__(self, num_classes):
        super(CNNModel, self).__init__()
        self.net = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Flatten(),
            nn.Linear(64 * (IMG_SIZE // 4) * (IMG_SIZE // 4), 128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, num_classes)
        )
    def forward(self, x):
        return self.net(x)
# Reconstruct class_names in training order
class_names = ['mango_Anthracnose',
 'mango_Die Back',
 'mango_Healthy',
 'mango_Sooty Mould',
 'mango_Gall Midge',
 'mango_Cutting Weevil',
 'mango_Powdery Mildew',
 'mango_Bacterial Canker']
# Load model
model = CNNModel(num_classes=8).to(DEVICE)
model.load_state_dict(torch.load("model/plant_disease_model.pth", map_location=DEVICE))
model.eval()
# Prediction function
def predict_image(img_path):
    transform = transforms.Compose([
        transforms.Resize((IMG_SIZE, IMG_SIZE)),
        transforms.ToTensor()
    ])
    image = Image.open(img_path).convert("RGB")
    image_tensor = transform(image).unsqueeze(0).to(DEVICE)

    with torch.no_grad():
        outputs = model(image_tensor)
        probs = torch.nn.functional.softmax(outputs, dim=1)
        confidence, predicted_idx = torch.max(probs, 1)

    predicted_class = class_names[predicted_idx.item()]
    return {
        "class": predicted_class,
        "confidence": confidence.item(),
        "diagnosis": DIAGNOSIS.get(predicted_class, "No info available"),
        "treatment": TREATMENTS.get(predicted_class, "No info available")
    }
