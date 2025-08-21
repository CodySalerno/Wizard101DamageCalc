import { Injectable } from "@angular/core";
import { openDB, IDBPDatabase } from "idb";
import type { AnySpell } from "../models/spells";
import type { Enemy } from "../models/enemy";

type WizardDB = {
  spells: AnySpell;
  enemies: Enemy;
  settings: { id: string; value: any };
};

@Injectable({ providedIn: "root" })
export class DbService {
  private dbPromise: Promise<IDBPDatabase>;

  constructor() {
    this.dbPromise = openDB("w101-calc", 1, {
      upgrade(db) {
        if (!db.objectStoreNames.contains("spells")) {
          db.createObjectStore("spells", { keyPath: "name" });
        }
        if (!db.objectStoreNames.contains("enemies")) {
          db.createObjectStore("enemies", { keyPath: "name" });
        }
        if (!db.objectStoreNames.contains("settings")) {
          db.createObjectStore("settings", { keyPath: "id" });
        }
      }
    });
  }

  async upsertSpell(spell: AnySpell) {
    const db = await this.dbPromise;
    return db.put("spells", spell);
  }
  async getSpell(name: string) {
    const db = await this.dbPromise;
    return db.get("spells", name) as Promise<AnySpell | undefined>;
  }
  async listSpells() {
    const db = await this.dbPromise;
    return db.getAll("spells") as Promise<AnySpell[]>;
  }

  async upsertEnemy(enemy: Enemy) {
    const db = await this.dbPromise;
    return db.put("enemies", enemy);
  }
  async listEnemies() {
    const db = await this.dbPromise;
    return db.getAll("enemies") as Promise<Enemy[]>;
  }

  async setSetting<T>(id: string, value: T) {
    const db = await this.dbPromise;
    return db.put("settings", { id, value });
  }
  async getSetting<T>(id: string): Promise<T | undefined> {
    const db = await this.dbPromise;
    const row = await db.get("settings", id) as { id: string; value: T } | undefined;
    return row?.value;
  }
}
