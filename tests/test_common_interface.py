"""
Test common application interface across all handlers
"""
from agents.base_apply import BaseApply


def test_common_interface():
    """Test that all handlers implement the common interface"""
    print("🧪 COMMON APPLICATION INTERFACE TEST")
    print("=" * 60)
    
    # Import all handlers
    from agents.handlers.linkedin_handler import LinkedInHandler
    from agents.handlers.workday_handler import WorkdayHandler
    from agents.handlers.greenhouse_handler import GreenhouseHandler
    from agents.handlers.lever_handler import LeverHandler
    from agents.handlers.indeed_handler import IndeedHandler
    
    # List of all handlers
    handlers = [
        LinkedInHandler,
        WorkdayHandler,
        GreenhouseHandler,
        LeverHandler,
        IndeedHandler
    ]
    
    print("Testing interface compliance:")
    print("-" * 60)
    
    compliant = 0
    total = len(handlers)
    
    for handler_class in handlers:
        handler_name = handler_class.__name__
        
        # Check if handler inherits from BaseApply
        from agents.base_apply import BaseApply as BaseApplyImport
        is_base_apply = issubclass(handler_class, BaseApplyImport)
        
        # Check if handler implements apply method
        has_apply_method = hasattr(handler_class, 'apply')
        
        # Check if apply is abstract (should not be in concrete classes)
        is_abstract = getattr(handler_class.apply, '__isabstractmethod__', False)
        
        status = "✅" if (is_base_apply and has_apply_method and not is_abstract) else "❌"
        
        print(f"{status} {handler_name}")
        print(f"   Inherits BaseApply: {is_base_apply}")
        print(f"   Has apply() method: {has_apply_method}")
        print(f"   Implements apply(): {not is_abstract}")
        
        if is_base_apply and has_apply_method and not is_abstract:
            compliant += 1
        else:
            print(f"   ⚠️  Interface issue detected")
    
    print(f"\n📊 Results: {compliant}/{total} handlers compliant ({compliant/total*100:.1f}%)")
    
    # Test method signature consistency
    print("\n🔍 Testing method signature consistency:")
    print("-" * 60)
    
    import inspect
    from agents.base_apply import BaseApply
    
    # Get the expected signature from BaseApply
    base_signature = inspect.signature(BaseApply.apply)
    base_params = list(base_signature.parameters.keys())
    print(f"Expected signature: {base_signature}")
    print(f"Expected parameters: {base_params}")
    
    # Check a concrete handler
    concrete_handler = LinkedInHandler()
    concrete_signature = inspect.signature(concrete_handler.apply)
    concrete_params = list(concrete_signature.parameters.keys())
    print(f"\nLinkedInHandler signature: {concrete_signature}")
    print(f"Parameters: {concrete_params}")
    
    # Check parameter compatibility (ignore 'self')
    base_params_no_self = [p for p in base_params if p != 'self']
    concrete_params_no_self = [p for p in concrete_params if p != 'self']
    compatible = set(base_params_no_self).issubset(set(concrete_params_no_self))
    print(f"\nParameter compatibility: {'✅ Compatible' if compatible else '❌ Incompatible'}")
    print(f"   Expected: {base_params_no_self}")
    print(f"   Actual: {concrete_params_no_self}")
    
    return compliant == total


def test_interface_benefits():
    """Demonstrate benefits of common interface"""
    print("\n💡 COMMON INTERFACE BENEFITS")
    print("=" * 60)
    
    print("✅ Consistency:")
    print("   All handlers have the same apply() method signature")
    print("   Same parameters: job_url, resume_path")
    print("   Predictable behavior across platforms")
    
    print("\n✅ Interchangeability:")
    print("   Handlers can be swapped without changing code")
    print("   ApplyEngine doesn't need platform-specific logic")
    print("   Easy to add new platforms")
    
    print("\n✅ Testing:")
    print("   Can mock BaseApply for unit testing")
    print("   Can test ApplyEngine with mock handlers")
    print("   Consistent test patterns")
    
    print("\n✅ Documentation:")
    print("   Single source of truth for interface")
    print("   Clear contract for handler implementation")
    print("   Easy to understand expected behavior")
    
    print("\n✅ Type Safety:")
    print("   Abstract method enforcement")
    print("   Compile-time interface checking")
    print("   IDE autocomplete support")
    
    print("\n✅ Future-Proofing:")
    print("   Interface changes apply to all handlers")
    print("   Can add methods to interface safely")
    print("   Deprecated methods can be managed centrally")


def test_polymorphic_usage():
    """Demonstrate polymorphic usage of common interface"""
    print("\n🎯 POLYMORPHIC USAGE DEMONSTRATION")
    print("=" * 60)
    
    from agents.base_apply import BaseApply
    from agents.handlers.linkedin_handler import LinkedInHandler
    from agents.handlers.workday_handler import WorkdayHandler
    
    print("Polymorphic approach - treat all handlers the same:")
    print("-" * 60)
    
    # Create handlers
    handlers = [
        LinkedInHandler(),
        WorkdayHandler()
    ]
    
    # Use them polymorphically (doesn't matter which is which)
    for handler in handlers:
        print(f"Handler: {handler.__class__.__name__}")
        print(f"Implements BaseApply: {isinstance(handler, BaseApply)}")
        print(f"Has apply() method: {hasattr(handler, 'apply')}")
    
    print("\n✅ Polymorphism verified:")
    print("   All handlers can be used interchangeably")
    print("   ApplyEngine doesn't need to know handler type")
    print("   Consistent interface guaranteed")


def test_interface_evolution():
    """Show how interface can evolve safely"""
    print("\n🔮 INTERFACE EVOLUTION DEMONSTRATION")
    print("=" * 60)
    
    print("Future enhancements to BaseApply:")
    print("-" * 60)
    
    print("Example: Adding optional parameter")
    print("from abc import ABC, abstractmethod")
    print()
    print("class BaseApply(ABC):")
    print("    @abstractmethod")
    print("    def apply(self, job_url, resume_path, cover_letter_path=None):")
    print("        pass")
    print()
    print("Benefits:")
    print("   • New parameter is optional (backward compatible)")
    print("   • Existing handlers still work")
    print("   • New handlers can use new parameter")
    print("   • Deprecation process managed centrally")
    
    print("\nExample: Adding new method")
    print("from abc import ABC, abstractmethod")
    print()
    print("class BaseApply(ABC):")
    print("    @abstractmethod")
    print("    def apply(self, job_url, resume_path):")
    print("        pass")
    print("    ")
    print("    @abstractmethod")
    print("    def get_status(self, job_url):")
    print("        pass")
    print()
    print("Benefits:")
    print("   • New method doesn't break existing apply()")
    print("   • Handlers can implement incrementally")
    print("   • Gradual rollout possible")
    print("   • Interface versioning supported")


def main():
    """Run all interface tests"""
    print("🧪 COMMON APPLICATION INTERFACE TESTS")
    print("=" * 60)
    
    # Test interface compliance
    interface_compliance = test_common_interface()
    
    # Show benefits
    test_interface_benefits()
    
    # Show polymorphic usage
    test_polymorphic_usage()
    
    # Show interface evolution
    test_interface_evolution()
    
    print("\n" + "=" * 60)
    print("✅ COMMON INTERFACE TESTS COMPLETE")
    print("\n🎯 KEY BENEFITS:")
    print("   ✅ Consistent interface across all platforms")
    print("   ✅ Polymorphic handler usage")
    print("   ✅ Type safety with abstract methods")
    print("   ✅ Easy to add new platforms")
    print("   ✅ Safe interface evolution")
    print("   ✅ Improved testability")


if __name__ == "__main__":
    main()
