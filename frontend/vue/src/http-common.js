import axios from "axios";
export default axios.create({
  // for-deployment
  baseURL: `http://${window.location.host}/api`,
  // for-development
  // baseURL: "http://127.0.0.1:8000/",
  headers: {
    "Content-type": "application/json"
  }
});
