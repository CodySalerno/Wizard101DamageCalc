import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { DbService } from '../../services/db.service';
import { AnySpell } from '../../models/spells';
import { SCHOOLS } from '../../constants/schools';

@Component({
  selector: 'app-spells-list',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './spells-list.component.html',
  styleUrls: ['./spells-list.component.css'],
})
export class SpellsListComponent implements OnInit {
  spells: AnySpell[] = [];
  filteredSpells: AnySpell[] = [];

  SCHOOLS = SCHOOLS;
  TYPES = ['Standard', 'Multiplier', 'Percent Buff'] as const;

  // Filter state
  selectedSchools: string[] = [...this.SCHOOLS];
  selectedTypes: string[] = [...this.TYPES];
  multiTargetFilter: boolean = false;

  minFlatDamage?: number;
  maxFlatDamage?: number;
  minMultiplier?: number;
  maxMultiplier?: number;
  minPercentBuff?: number;
  maxPercentBuff?: number;
  minPipCost?: number;
  maxPipCost?: number;

  constructor(private db: DbService) {}

  async ngOnInit() {
    this.spells = await this.db.listSpells();
    this.applyFilters();
  }

  onSchoolToggle(evt: Event, school: string) {
    const checked = (evt.target as HTMLInputElement).checked;
    if (checked) {
      if (!this.selectedSchools.includes(school)) {
        this.selectedSchools = [...this.selectedSchools, school];
      }
    } else {
      this.selectedSchools = this.selectedSchools.filter((s) => s !== school);
    }
  }

  onTypeToggle(evt: Event, type: string) {
    const checked = (evt.target as HTMLInputElement).checked;
    if (checked) {
      if (!this.selectedTypes.includes(type)) {
        this.selectedTypes = [...this.selectedTypes, type];
      }
    } else {
      this.selectedTypes = this.selectedTypes.filter((t) => t !== type);
    }
  }

  applyFilters() {
    this.filteredSpells = this.spells.filter((spell) => {
      // School
      if (!this.selectedSchools.includes(spell.school)) return false;
      // Type
      if (!this.selectedTypes.includes(spell.type)) return false;
      // Multi-target
      if (this.multiTargetFilter && !spell.multiTarget) return false;

      // Damage / cost (Standard)
      if (spell.type === 'Standard') {
        if (this.minFlatDamage !== undefined && spell.minDam < this.minFlatDamage) return false;
        if (this.maxFlatDamage !== undefined && spell.maxDam > this.maxFlatDamage) return false;
        if (this.minPipCost !== undefined && spell.cost < this.minPipCost) return false;
        if (this.maxPipCost !== undefined && spell.cost > this.maxPipCost) return false;
      }

      // Multiplier
      if (spell.type === 'Multiplier') {
        if (this.minMultiplier !== undefined && spell.multiplier < this.minMultiplier) return false;
        if (this.maxMultiplier !== undefined && spell.multiplier > this.maxMultiplier) return false;
      }

      // Percent Buff
      if (spell.type === 'Percent Buff') {
        if (this.minPercentBuff !== undefined && spell.percent < this.minPercentBuff) return false;
        if (this.maxPercentBuff !== undefined && spell.percent > this.maxPercentBuff) return false;
        if (this.minPipCost !== undefined && spell.cost < this.minPipCost) return false;
        if (this.maxPipCost !== undefined && spell.cost > this.maxPipCost) return false;
      }

      return true;
    });
  }

  /* New: convenience reset */
  resetFilters() {
    this.selectedSchools = [...this.SCHOOLS];
    this.selectedTypes = [...this.TYPES];
    this.multiTargetFilter = false;
    this.minFlatDamage = this.maxFlatDamage = undefined;
    this.minMultiplier = this.maxMultiplier = undefined;
    this.minPercentBuff = this.maxPercentBuff = undefined;
    this.minPipCost = this.maxPipCost = undefined;
    this.applyFilters();
  }
}
