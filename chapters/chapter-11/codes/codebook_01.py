"""Ch-11 Project 1: Variational quantum classifier — binary classification."""
import numpy as np
from qiskit.circuit.library import ZZFeatureMap, RealAmplitudes
from qiskit.quantum_info import Statevector, SparsePauliOp

np.random.seed(42)
n_q = 2
fmap   = ZZFeatureMap(n_q, reps=1)
ansatz = RealAmplitudes(n_q, reps=2)
n_p    = ansatz.num_parameters

H = SparsePauliOp('ZI').to_matrix()

def predict(x, theta):
    qc = fmap.assign_parameters(x).compose(ansatz.assign_parameters(theta))
    sv = Statevector(qc).data
    return float(np.real(sv.conj() @ H @ sv))

def loss(theta, X, y):
    return sum((predict(x,theta)-yi)**2 for x,yi in zip(X,y)) / len(y)

# Simple dataset: 4 labeled points in feature space
X_tr = np.array([[0.5,0.5],[-0.5,-0.5],[0.5,-0.5],[-0.5,0.5]])
y_tr = np.array([1.0, 1.0, -1.0, -1.0])

theta = np.random.uniform(0, 2*np.pi, n_p); lr = 0.1
print(f"{'step':>5}  {'loss':>10}  {'acc':>8}")
for step in range(40):
    grads = np.zeros(n_p)
    for k in range(n_p):
        tp,tm = theta.copy(), theta.copy(); tp[k]+=np.pi/2; tm[k]-=np.pi/2
        grads[k] = sum((predict(x,tp)-y)**2-(predict(x,tm)-y)**2
                       for x,y in zip(X_tr,y_tr)) / len(y_tr) * 0.5
    theta -= lr*grads
    if step % 8 == 0:
        l = loss(theta, X_tr, y_tr)
        a = sum((predict(x,theta)*y>0) for x,y in zip(X_tr,y_tr)) / len(y_tr)
        print(f"  {step:3d}  {l:10.6f}  {a:8.2f}")
