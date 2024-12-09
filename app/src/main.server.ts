import { bootstrapApplication } from '@angular/platform-browser';
import { config } from './app/app.config.server';
import { PaymentListComponent } from './app/components/payment-list/payment-list.component';
import { AppComponent } from './app/app.component';

const bootstrap = () => bootstrapApplication(AppComponent, config);

export default bootstrap;