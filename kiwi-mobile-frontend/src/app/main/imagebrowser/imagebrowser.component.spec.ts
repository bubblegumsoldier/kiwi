import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ImagebrowserComponent } from './imagebrowser.component';

describe('ImagebrowserComponent', () => {
  let component: ImagebrowserComponent;
  let fixture: ComponentFixture<ImagebrowserComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ImagebrowserComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ImagebrowserComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
