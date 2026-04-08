import gradio as gr
from env import FraudEnv
from policy import decide


def run_system(level):
    # -------------------------------
    # 📥 Load dataset dynamically
    # -------------------------------
    if level == "easy":
        from tasks.easy import transactions
    elif level == "medium":
        from tasks.medium import transactions
    else:
        from tasks.hard import transactions

    env = FraudEnv(transactions)
    state = env.reset()

    output = []
    frauds = 0
    correct = 0
    total = 0
    step_count = 1

    output.append("🤖 AI Model analyzing transaction patterns...\n")
    output.append("=== TRANSACTION ANALYSIS ===\n")

    # -------------------------------
    # 🔄 Simulation loop
    # -------------------------------
    while True:
        action, risk, reason = decide(state)

        result = env.step(action)
        state = result.next_state
        reward = result.reward
        done = result.done

        action_name = env.ACTIONS[action]

        # 🎯 Confidence level
        confidence = (
            "HIGH" if risk > 0.7 else
            "MEDIUM" if risk > 0.4 else
            "LOW"
        )

        # 🎨 Emoji
        emoji = "✅" if action_name == "approve" else "⚠️" if action_name == "flag" else "🚫"

        # 📊 Fraud count
        if action_name == "block":
            frauds += 1

        # 📈 Accuracy tracking
        total += 1
        if "label" in transactions[step_count - 1]:
            if action_name == transactions[step_count - 1]["label"]:
                correct += 1

        log = (
            f"Transaction {step_count} → {emoji} {action_name.upper()} | "
            f"Risk: {risk:.2f} ({confidence}) | "
            f"Reason: {reason} | "
            f"Reward: {reward}"
        )

        output.append(log)
        step_count += 1

        if done:
            break

    # -------------------------------
    # 📊 Final Report
    # -------------------------------
    accuracy = (correct / total) * 100 if total > 0 else 0

    output.append("\n🔍 AI Decision Summary:")
    output.append("System analyzed patterns using risk scoring + rule-based logic.\n")

    output.append("=== FINAL REPORT ===")
    output.append(f"Total Transactions: {total}")
    output.append(f"Frauds Detected: {frauds}")
    output.append(f"Accuracy: {accuracy:.2f}%")
    output.append(f"Total Reward: {env._total_reward}")

    return "\n".join(output)


# -------------------------------
# 🎨 Gradio UI
# -------------------------------
gr.Interface(
    fn=run_system,
    inputs=gr.Dropdown(
        ["easy", "medium", "hard"],
        label="Select Difficulty Level"
    ),
    outputs="text",
    title="💳 Fraud Detection AI System",
    description="AI system with risk scoring, explainability, performance metrics, and multi-level datasets",
    submit_btn="🚀 Run Fraud Detection"
).launch()