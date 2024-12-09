import { bootstrapApplication } from '@angular/platform-browser';
import { appConfig } from './app/app.config';
import { AppComponent } from './app/app.component';

bootstrapApplication(AppComponent, appConfig)
  .catch((err) => console.error(err));
// import { PaymentListComponent } from './app/components/payment-list/payment-list.component';

// bootstrapApplication(PaymentListComponent, appConfig).catch((err) => console.error(err));