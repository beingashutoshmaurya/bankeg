// src/services/notificationService.js
import api from "./api";

export default {
  async getAll(customerId) {
    const res = await api.get(`/api/notifications/${customerId}`);
    return res.data;
  },

  async markAsRead(notificationId) {
    await api.put(`/api/notifications/${notificationId}/read`);
  },

  async delete(notificationId) {
    await api.delete(`/api/notifications/${notificationId}`);
  },
};
