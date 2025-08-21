import { School } from "./spells";

export interface Enemy {
  name: string;
  health: number;
  resists?: Partial<Record<School, number>>;    // e.g. 25 for 25% resist
  weaknesses?: Partial<Record<School, number>>; // e.g. 25 for +25% dmg taken
}
