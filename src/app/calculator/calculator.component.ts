import { Component, OnInit } from '@angular/core';
import { CalcService } from '../services/calc.service';

@Component({
  selector: 'app-calculator',
  template: `
    <h2>Damage Test</h2>
    <p>Result: {{ result }}</p>
  `
})
export class CalculatorComponent implements OnInit {
  result = 0;

  constructor(private calc: CalcService) {}

  ngOnInit() {
    // quick dummy test — just call something to confirm it works
    this.result = this.calc.buffStandard(
      { multiplier: 1.5, cost: 1, names: ['Blade'], multiTarget: true },
      { name: 'Fire Cat', type: 'Standard', multiTarget: false, school: 'Fire', cost: 1, minDam: 80, maxDam: 120 },
      { gearPerc: 20, gearFlat: 10 }
    ).maxDam;
  }
}
