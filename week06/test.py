import torch
print(('gpu' if torch.cuda.is_available() else 'cpu') + ' is available')