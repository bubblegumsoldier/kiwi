import { TestBed, inject } from '@angular/core/testing';

import { UsermanagerService } from './usermanager.service';

describe('UsermanagerService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [UsermanagerService]
    });
  });

  it('should be created', inject([UsermanagerService], (service: UsermanagerService) => {
    expect(service).toBeTruthy();
  }));
});
