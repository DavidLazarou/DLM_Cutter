# 📌 Lagrangian Formulation for Portfolio Optimization

## 🎯 Objective

Minimize the **portfolio variance**:

\[
\min_{\mathbf{w}} \quad \mathbf{w}^\top \Sigma \mathbf{w}
\]

Where:
- \(\mathbf{w}\): vector of portfolio weights
- \(\Sigma\): covariance matrix of asset returns

---

## 📏 Constraints

1. **Expected return**:
\[
\mathbf{w}^\top \mu = R_t
\]

2. **Full investment**:
\[
\mathbf{w}^\top \mathbf{1} = 1
\]

---

## 🧠 Lagrangian Function

The Lagrangian is defined as:

\[
\mathcal{L}(\mathbf{w}, \lambda, \gamma) = \mathbf{w}^\top \Sigma \mathbf{w} - \lambda (\mathbf{w}^\top \mu - R_t) - \gamma (\mathbf{w}^\top \mathbf{1} - 1)
\]

Where:
- \(\lambda\): Lagrange multiplier for expected return constraint
- \(\gamma\): Lagrange multiplier for full investment constraint

---

## 🧮 First-Order Conditions

Taking partial derivatives:

\[
\nabla_{\mathbf{w}} \mathcal{L} = 2\Sigma \mathbf{w} - \lambda \mu - \gamma \mathbf{1} = 0
\]

\[
\nabla_{\lambda} \mathcal{L} = \mathbf{w}^\top \mu - R_t = 0
\]

\[
\nabla_{\gamma} \mathcal{L} = \mathbf{w}^\top \mathbf{1} - 1 = 0
\]

---

## ✅ Next Step

Solve the system of equations for optimal weights \(\mathbf{w}^*\), given a target return \(R_t\).

Move to `02_analytical_solution.md` to plug this into a linear system.

