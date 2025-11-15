import Stripe from 'stripe';
import { NextRequest, NextResponse } from 'next/server';

export async function POST(req: NextRequest) {
  try {
    const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
      apiVersion: '2024-06-20',
    });

    const sig = req.headers.get('stripe-signature');
    if (!sig) {
      return NextResponse.json(
        { error: 'No signature provided' },
        { status: 400 }
      );
    }

    const buf = Buffer.from(await req.arrayBuffer());
    let event: Stripe.Event;

    try {
      event = stripe.webhooks.constructEvent(
        buf,
        sig,
        process.env.STRIPE_WEBHOOK_SECRET!
      );
    } catch (err) {
      const error = err as Error;
      console.error('Webhook signature verification failed:', error.message);
      return NextResponse.json(
        { error: `Webhook Error: ${error.message}` },
        { status: 400 }
      );
    }

    // Handle checkout.session.completed event
    if (event.type === 'checkout.session.completed') {
      const session = event.data.object as Stripe.Checkout.Session;
      const priceId = session.metadata?.price_id;
      const plan = session.metadata?.plan;
      const templateRepo = session.metadata?.template_repo;

      console.log('Checkout completed:', {
        sessionId: session.id,
        customerEmail: session.customer_email,
        priceId,
        plan,
        templateRepo,
      });

      // Call provisioning API
      if (priceId && plan && templateRepo) {
        try {
          const provisionResponse = await fetch(
            `${process.env.NEXT_PUBLIC_BASE_URL || 'http://localhost:3000'}/api/provision`,
            {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify({
                customerEmail: session.customer_email,
                plan,
                templateRepo,
                priceId,
              }),
            }
          );

          const provisionResult = await provisionResponse.json();
          console.log('Provisioning result:', provisionResult);
        } catch (err) {
          console.error('Provisioning failed:', err);
        }
      }
    }

    // Handle subscription events (invoice.paid for upgrades)
    if (event.type === 'invoice.paid') {
      const invoice = event.data.object as Stripe.Invoice;
      console.log('Invoice paid:', {
        invoiceId: invoice.id,
        customerEmail: invoice.customer_email,
        subscriptionId: invoice.subscription,
      });
      // Handle subscription upgrades/renewals here
    }

    return NextResponse.json({ received: true });
  } catch (err) {
    const error = err as Error;
    console.error('Webhook processing error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
