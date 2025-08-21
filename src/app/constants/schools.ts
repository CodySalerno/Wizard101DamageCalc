export const SCHOOLS = [
  "Fire",
  "Ice",
  "Storm",
  "Myth",
  "Life",
  "Death",
  "Balance"
] as const;

export type School = (typeof SCHOOLS)[number];
