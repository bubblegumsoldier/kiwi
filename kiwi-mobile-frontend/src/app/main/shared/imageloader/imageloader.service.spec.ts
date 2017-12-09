import { TestBed, inject } from '@angular/core/testing';

import { ImageloaderService } from './imageloader.service';

describe('ImageloaderService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [ImageloaderService]
    });
  });

  it('should be created', inject([ImageloaderService], (service: ImageloaderService) => {
    expect(service).toBeTruthy();
  }));
});
