// Tiny demo to call predict and process endpoints
async function predictAndProcess(amount, merchant, location) {
  const predictRes = await fetch('/api/transaction/predict', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ amount, merchant, location })
  });

  const pred = await predictRes.json();
  console.log('Prediction:', pred);

  // If flagged, show confirm dialog in UI
  let userApproved = false;
  if (pred.is_fraud) {
    userApproved = confirm('Transaction flagged as potential fraud. Approve?');
  }

  const processRes = await fetch('/api/transaction/process', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ transaction_data: pred.transaction_data, fraud_probability: pred.fraud_probability, user_approved: userApproved })
  });

  const processed = await processRes.json();
  console.log('Processed:', processed);
  return processed;
}

// Example usage (uncomment to run in browser console):
// predictAndProcess(25.5, 'Example Merchant', 'SomeCity');
