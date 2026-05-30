export const env = {
  NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1",
};

if (typeof window !== "undefined") {
  console.log("Environment loaded:", env);
}

