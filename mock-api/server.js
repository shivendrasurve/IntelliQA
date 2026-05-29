const express = require('express');
const app = express();
app.use(express.json());

let payments = {};
let accounts = {
  "acc_001": { id: "acc_001", owner: "John Doe",   balance: 5000 },
  "acc_002": { id: "acc_002", owner: "Jane Smith", balance: 3000 },
};

app.post('/payments', (req, res) => {
  const { amount, currency, account_id } = req.body;
  if (!amount || amount <= 0)
    return res.status(400).json({ error: "Invalid amount" });
  if (!currency)
    return res.status(400).json({ error: "Currency is required" });
  if (!accounts[account_id])
    return res.status(404).json({ error: "Account not found" });
  if (accounts[account_id].balance < amount)
    return res.status(400).json({ error: "Insufficient funds" });
  const id = "pay_" + Date.now();
  payments[id] = { id, amount, currency, account_id, status: "success" };
  accounts[account_id].balance -= amount;
  res.status(201).json(payments[id]);
});

app.get('/payments/:id', (req, res) => {
  const payment = payments[req.params.id];
  if (!payment) return res.status(404).json({ error: "Payment not found" });
  res.json(payment);
});

app.post('/refunds', (req, res) => {
  const { payment_id, amount } = req.body;
  const payment = payments[payment_id];
  if (!payment) return res.status(404).json({ error: "Payment not found" });
  if (amount > payment.amount)
    return res.status(400).json({ error: "Refund exceeds original payment" });
  accounts[payment.account_id].balance += amount;
  res.status(201).json({ id: "ref_" + Date.now(), payment_id, amount, status: "refunded" });
});

app.get('/accounts/:id', (req, res) => {
  const account = accounts[req.params.id];
  if (!account) return res.status(404).json({ error: "Account not found" });
  res.json(account);
});

app.post('/transfers', (req, res) => {
  const { from_account, to_account, amount } = req.body;
  if (!accounts[from_account] || !accounts[to_account])
    return res.status(404).json({ error: "Account not found" });
  if (accounts[from_account].balance < amount)
    return res.status(400).json({ error: "Insufficient funds" });
  accounts[from_account].balance -= amount;
  accounts[to_account].balance   += amount;
  res.status(200).json({ status: "success", from: from_account, to: to_account, amount });
});

app.listen(3000, () => console.log("✅ Mock FinTech API running → http://localhost:3000"));
