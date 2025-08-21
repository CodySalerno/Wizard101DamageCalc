import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SpellsListComponent } from './spells-list.component';

describe('SpellsListComponent', () => {
  let component: SpellsListComponent;
  let fixture: ComponentFixture<SpellsListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SpellsListComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SpellsListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
