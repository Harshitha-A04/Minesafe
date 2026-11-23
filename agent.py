class MineSafeAgent:
    def analyze_environment(self, gas, temperature, battery, obstacle):
        alerts = []

        if gas > 25:
            alerts.append("💨 High gas level detected.")
        if temperature > 45:
            alerts.append("🌡️ Temperature is dangerously high.")
        if battery < 20:
            alerts.append("🔋 Robot battery is low.")
        if obstacle == 1:
            alerts.append("🚧 Obstacle in navigation path.")
        if not alerts:
            alerts.append("✅ All sensor readings are normal.")

        if gas > 25 or temperature > 45:
            action = "Stop the robot and evacuate the area."
        elif obstacle == 1:
            action = "Reroute the robot around the obstacle."
        elif battery < 20:
            action = "Return the robot to the charging station."
        else:
            action = "Continue normal operation."

        return {"alerts": alerts, "action": action}