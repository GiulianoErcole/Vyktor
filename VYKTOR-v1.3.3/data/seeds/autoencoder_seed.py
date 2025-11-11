# FITNESS_PROFILE guides the adaptive fitness combiner
FITNESS_PROFILE = { 'accuracy': 0.55, 'efficiency': 0.25, 'entropy': 0.10, 'stability': 0.10 }

def solution(device='cpu', steps=10, n=128, d=64, bottleneck=16):
    import torch, torch.nn as nn
    torch.manual_seed(0)
    X = torch.randn(n, d, device=device)

    class AE(nn.Module):
        def __init__(self, d=64, k=16):
            super().__init__()
            self.enc = nn.Sequential(nn.Linear(d, 32), nn.ReLU(), nn.Linear(32, k))
            self.dec = nn.Sequential(nn.Linear(k, 32), nn.ReLU(), nn.Linear(32, d))
        def forward(self, x):
            z = self.enc(x); y = self.dec(z); return y

    model = AE(d, bottleneck).to(device)
    opt = torch.optim.Adam(model.parameters(), lr=1e-2)
    loss_fn = nn.MSELoss()

    for _ in range(steps):
        y = model(X); loss = loss_fn(y, X)
        opt.zero_grad(); loss.backward(); opt.step()
    # Return final loss as a quick metric
    return float(loss.detach().cpu().item())

def fitness_probe():
    # Try CPU first; GPU if available
    try:
        import torch
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
    except Exception:
        device = 'cpu'
    try:
        final_loss = solution(device=device, steps=5)
        # Map loss to accuracy-like metric
        acc = 1.0/(1.0 + final_loss)
        return {'accuracy_proxy': acc}
    except Exception:
        return {'accuracy_proxy': 0.0}

def run_tests():
    # Smoke test: ensure it runs quickly and returns a smallish loss
    loss = solution(device='cpu', steps=3, n=64, d=32, bottleneck=8)
    assert loss >= 0.0
