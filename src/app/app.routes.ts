import { Routes } from '@angular/router';
import { HomeComponent } from './pages/home/home.component';
import { SpellsListComponent } from './pages/spells-list/spells-list.component';
import { SpellFormComponent } from './pages/spell-form/spell-form.component';
import { CalculatorComponent } from './pages/calculator/calculator.component';

export const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'spells', component: SpellsListComponent },
  { path: 'spells/new', component: SpellFormComponent },
  { path: 'calculator', component: CalculatorComponent },
  { path: '**', redirectTo: '' },
];
