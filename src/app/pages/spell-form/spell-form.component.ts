import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { DbService } from '../../services/db.service';
import type { AnySpell } from '../../models/spells';

@Component({
  selector: 'app-spell-form',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './spell-form.component.html',
})
export class SpellFormComponent {
  type: 'Standard'|'Multiplier'|'Percent Buff' = 'Standard';
  name = '';
  school: any = 'Fire';
  cost?: number;
  minDam?: number;
  maxDam?: number;
  multiplier?: number;
  percent?: number;
  multiTarget = false;

  schools = ['Balance','Storm','Fire','Life','Death','Ice','Myth'];

  constructor(private db: DbService) {}

  async save() {
    if (!this.name) return;
    let payload: AnySpell;

    if (this.type === 'Standard') {
      payload = { name: this.name, type: 'Standard', school: this.school, multiTarget: this.multiTarget,
                  cost: this.cost ?? 0, minDam: this.minDam ?? 0, maxDam: this.maxDam ?? 0 };
    } else if (this.type === 'Multiplier') {
      payload = { name: this.name, type: 'Multiplier', school: this.school, multiTarget: this.multiTarget,
                  multiplier: this.multiplier ?? 0 };
    } else {
      payload = { name: this.name, type: 'Percent Buff', school: this.school, multiTarget: this.multiTarget,
                  cost: this.cost ?? 0, percent: this.percent ?? 0 };
    }

    await this.db.upsertSpell(payload);
    this.name = ''; this.cost = this.minDam = this.maxDam = undefined;
    this.multiplier = this.percent = undefined;
    alert('Saved!');
  }
}
