from transformers import AutoTokenizer, AutoModelForSequenceClassification, AdamW
from torch.nn import CrossEntropyLoss
from torch.utils.data import Dataset, DataLoader
import torch

class TextDataset(Dataset):
    def __init__(self, texts, labels, tokenizer):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        label = self.labels[idx]
        encoding = self.tokenizer.encode_plus(
            text,
            truncation=True,
            padding='max_length',
            max_length=512,
            return_tensors='pt'
        )
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(label, dtype=torch.long)
        }

def train_model(X_train, y_train, model_name):
    # Convert Series to lists
    X_train = X_train.tolist()
    y_train = y_train.tolist()

    # Load model and tokenizer
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # Convert data to tensors
    dataset = TextDataset(X_train, y_train, tokenizer)
    dataloader = DataLoader(dataset, batch_size=64)

    # Define optimizer
    optimizer = AdamW(model.parameters(), lr=1e-5)

    # Define loss function
    loss_fn = CrossEntropyLoss()

    # Training loop
    for epoch in range(1):  # Number of epochs
        for batch in dataloader:
            input_ids = batch['input_ids']
            attention_mask = batch['attention_mask']
            labels = batch['labels']

            # Forward pass
            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            logits = outputs.logits

            # Compute loss
            loss = loss_fn(logits.view(-1, model.config.num_labels), labels.view(-1))

            # Backward pass and optimization
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

    return model

def predict(model, X_test, model_name):
    # Convert Series to list
    X_test = X_test.tolist()

    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # Convert data to tensors
    dataset = TextDataset(X_test, [0]*len(X_test), tokenizer)  # Dummy labels for prediction
    dataloader = DataLoader(dataset, batch_size=64)

    predictions = []

    # Prediction loop
    model.eval()
    with torch.no_grad():
        for batch in dataloader:
            input_ids = batch['input_ids']
            attention_mask = batch['attention_mask']

            # Forward pass
            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            logits = outputs.logits

            # Get predictions
            _, preds = torch.max(logits.view(-1, model.config.num_labels), dim=1)
            predictions.extend(preds.tolist())

    return predictions
