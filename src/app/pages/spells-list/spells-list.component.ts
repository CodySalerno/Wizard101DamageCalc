import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DbService } from '../../services/db.service';
import type { AnySpell } from '../../models/spells';

@Component({
  selector: 'app-spells-list',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './spells-list.component.html',
})
export class SpellsListComponent implements OnInit {
  spells: AnySpell[] = [];
  loading = true;

  constructor(private db: DbService) {}

  async ngOnInit() {
    this.spells = await this.db.listSpells();
    this.loading = false;
  }
}
