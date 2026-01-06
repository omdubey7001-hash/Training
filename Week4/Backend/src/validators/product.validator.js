import { z } from "zod";

export const createProductSchema = z.object({
  name: z
    .string()
    .min(2, "Name must be at least 2 characters")
    .max(100),

  description: z.string().optional(),

  price: z
    .number()
    .positive("Price must be greater than 0"),

  tags: z.array(z.string()).optional()
});
