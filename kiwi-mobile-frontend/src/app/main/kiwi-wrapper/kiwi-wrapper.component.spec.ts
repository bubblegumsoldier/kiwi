import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { KiwiWrapperComponent } from './kiwi-wrapper.component';

describe('KiwiWrapperComponent', () => {
  let component: KiwiWrapperComponent;
  let fixture: ComponentFixture<KiwiWrapperComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ KiwiWrapperComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(KiwiWrapperComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
