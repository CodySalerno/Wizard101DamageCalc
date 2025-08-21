import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SpellsFormComponent } from './spells-form.component';

describe('SpellsFormComponent', () => {
  let component: SpellsFormComponent;
  let fixture: ComponentFixture<SpellsFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SpellsFormComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SpellsFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
