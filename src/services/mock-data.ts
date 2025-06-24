export const mockData = {
  deliveries: [
    { id: "D001", customer: "ABC Logistics", status: "delivered", onTime: true },
    { id: "D002", customer: "XYZ Corp", status: "in_transit", onTime: true },
    { id: "D003", customer: "Fast Foods Inc", status: "delayed", onTime: false }
  ],
  drivers: [
    { id: "DR001", name: "Mike Johnson", safetyScore: 95, status: "on_route" },
    { id: "DR002", name: "Sarah Martinez", safetyScore: 98, status: "available" }
  ],
  kpis: {
    totalDeliveries: 45,
    onTimeRate: 92,
    activeDrivers: 18,
    safetyScore: 87
  }
}; 