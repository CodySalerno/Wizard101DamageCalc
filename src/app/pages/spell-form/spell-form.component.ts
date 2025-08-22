import { AfterViewInit, Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { DbService } from '../../services/db.service';
import type { AnySpell } from '../../models/spells';
import { School, SCHOOLS } from "../../constants/schools";


const isNonNegativeInteger = (val: any): val is number =>
    typeof val === 'number' && Number.isInteger(val) && val >= 0;

@Component({
  selector: 'app-spell-form',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './spell-form.component.html',
  styleUrls: ['./spell-form.component.css']
})

export class SpellFormComponent implements AfterViewInit{
  type: 'Standard'|'Multiplier'|'Percent Buff' = 'Standard';
  name = '';
  school: School = 'Balance'; // TODO: Add preference setting for default school
  cost?: number;
  minDam?: number;
  maxDam?: number;
  multiplier?: number;
  percent?: number;
  multiTarget = false;
  SCHOOLS = SCHOOLS;
  didInit = false;
  flashSchool: School | null = null;

  ngAfterViewInit() {
    setTimeout(() => (this.didInit = true));
  }

  onFlashEnd() {
    this.flashSchool = null;
  }

  constructor(private db: DbService) {}

  
  //TODO: highlight invalid fields instead of returning
  async save() {
    if (!this.name.trim()) return;
    if (!SCHOOLS.includes(this.school)) return;
    let payload: AnySpell;

    if (this.type === 'Standard') {
      if (isNonNegativeInteger(this.cost) === false) return; // cost should be a non-negative integer
      if (isNonNegativeInteger(this.minDam) === false) return; // minDam should be a non-negative integer
      if (isNonNegativeInteger(this.maxDam) === false) return; // maxDam should be a non-negative integer
      if (this.minDam > this.maxDam) return; // minDam should not be greater than maxDam
      
      payload = { name: this.name, type: 'Standard', school: this.school, multiTarget: this.multiTarget,
                  cost: this.cost, minDam: this.minDam, maxDam: this.maxDam};
    } 
    
    else if (this.type === 'Multiplier') {
      if (isNonNegativeInteger(this.multiplier) === false) return; // multiplier should be a non-negative number

      payload = { name: this.name, type: 'Multiplier', school: this.school, multiTarget: this.multiTarget,
                  multiplier: this.multiplier ?? 0 };
    }
    
    else if (this.type === 'Percent Buff') {
      if (isNonNegativeInteger(this.cost) === false) return; // cost should be a non-negative integer
      if (isNonNegativeInteger(this.percent) === false || this.percent > 100) return; // percent should be between 0 and 100
      
      payload = { name: this.name, type: 'Percent Buff', school: this.school, multiTarget: this.multiTarget,
                  cost: this.cost ?? 0, percent: this.percent ?? 0 };
    }
    else {
      return; // Invalid type
    }

    await this.db.upsertSpell(payload);
    this.name = ''; this.cost = this.minDam = this.maxDam = undefined;
    this.multiplier = this.percent = undefined;
    this.flashSchool = this.school;
  }
}
