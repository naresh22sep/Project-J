#!/usr/bin/env python
"""
Check for and remove duplicate subscription plans
"""

from app import create_app, db
from app.auth.auth_models import SubscriptionPlan, SubscriptionFeature, UserSubscription
from sqlalchemy import func

def find_and_remove_duplicates():
    """Find and remove duplicate subscription plans"""
    try:
        print("🔍 Checking for duplicate subscription plans...")
        
        # Find duplicates by name
        duplicates_by_name = db.session.query(
            SubscriptionPlan.name,
            func.count(SubscriptionPlan.id).label('count')
        ).group_by(SubscriptionPlan.name).having(func.count(SubscriptionPlan.id) > 1).all()
        
        print(f"Found {len(duplicates_by_name)} plan names with duplicates:")
        for name, count in duplicates_by_name:
            print(f"  - '{name}': {count} instances")
        
        # Find duplicates by display_name
        duplicates_by_display = db.session.query(
            SubscriptionPlan.display_name,
            func.count(SubscriptionPlan.id).label('count')
        ).group_by(SubscriptionPlan.display_name).having(func.count(SubscriptionPlan.id) > 1).all()
        
        print(f"\nFound {len(duplicates_by_display)} display names with duplicates:")
        for display_name, count in duplicates_by_display:
            print(f"  - '{display_name}': {count} instances")
        
        # Get all plans ordered by creation date
        all_plans = SubscriptionPlan.query.order_by(SubscriptionPlan.created_at).all()
        print(f"\nTotal plans in database: {len(all_plans)}")
        
        # Show all plans
        print("\nAll Subscription Plans:")
        for i, plan in enumerate(all_plans, 1):
            users_count = UserSubscription.query.filter_by(plan_id=plan.id).count()
            features_count = SubscriptionFeature.query.filter_by(plan_id=plan.id).count()
            print(f"  {i:2d}. [{plan.id:2d}] {plan.display_name} ({plan.name}) - {plan.plan_type}")
            print(f"      Price: ${plan.price_monthly}/month, Users: {users_count}, Features: {features_count}")
            print(f"      Created: {plan.created_at}")
        
        # Identify plans to keep and remove
        plans_to_remove = []
        seen_names = set()
        
        for plan in all_plans:
            if plan.name in seen_names:
                # This is a duplicate
                users_count = UserSubscription.query.filter_by(plan_id=plan.id).count()
                if users_count == 0:  # Only remove if no users are subscribed
                    plans_to_remove.append(plan)
                else:
                    print(f"\n⚠️ Duplicate plan '{plan.display_name}' has {users_count} users - keeping it")
            else:
                seen_names.add(plan.name)
        
        if plans_to_remove:
            print(f"\n🗑️ Plans to remove ({len(plans_to_remove)}):")
            for plan in plans_to_remove:
                print(f"  - [{plan.id}] {plan.display_name} ({plan.name})")
            
            response = input(f"\nDo you want to remove these {len(plans_to_remove)} duplicate plans? (y/N): ")
            if response.lower() == 'y':
                removed_count = 0
                for plan in plans_to_remove:
                    # Remove associated features first
                    SubscriptionFeature.query.filter_by(plan_id=plan.id).delete()
                    # Remove the plan
                    db.session.delete(plan)
                    removed_count += 1
                    print(f"  ✅ Removed plan: {plan.display_name}")
                
                db.session.commit()
                print(f"\n🎉 Successfully removed {removed_count} duplicate plans!")
            else:
                print("\n❌ Operation cancelled")
        else:
            print("\n✅ No duplicate plans to remove (all duplicates have active users)")
        
        # Final count
        final_count = SubscriptionPlan.query.count()
        print(f"\nFinal plan count: {final_count}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        db.session.rollback()

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        find_and_remove_duplicates()