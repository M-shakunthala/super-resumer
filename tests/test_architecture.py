"""
Test platform detection and apply engine architecture
"""
from agents.platform_detector import PlatformDetector
from agents.apply_engine import ApplyEngine


def test_platform_detector():
    """Test platform detection from URLs"""
    print("🧪 PLATFORM DETECTOR TEST")
    print("=" * 60)
    
    detector = PlatformDetector()
    
    # Test URLs from different platforms
    test_urls = [
        {
            "url": "https://www.linkedin.com/jobs/view/python-developer-123456/",
            "expected": "linkedin"
        },
        {
            "url": "https://myworkdayjobs.com/techcorp/job/Python-Developer",
            "expected": "workday"
        },
        {
            "url": "https://boards.greenhouse.io/techcorp/jobs/123456",
            "expected": "greenhouse"
        },
        {
            "url": "https://jobs.lever.co/techcorp/python-developer",
            "expected": "lever"
        },
        {
            "url": "https://www.indeed.com/viewjob?jk=python-developer",
            "expected": "indeed"
        },
        {
            "url": "https://some-other-ats.com/job/123",
            "expected": "unknown"
        }
    ]
    
    print("Testing platform detection from URLs:")
    print("-" * 60)
    
    correct = 0
    total = len(test_urls)
    
    for test in test_urls:
        url = test['url']
        expected = test['expected']
        detected = detector.detect(url)
        
        status = "✅" if detected == expected else "❌"
        print(f"{status} {expected.upper():12} → {detected}")
        
        if detected == expected:
            correct += 1
    
    print(f"\n📊 Results: {correct}/{total} correct ({correct/total*100:.1f}%)")
    return correct == total


def test_apply_engine():
    """Test apply engine architecture"""
    print("\n🧪 APPLY ENGINE TEST")
    print("=" * 60)
    
    engine = ApplyEngine()
    
    # Check supported platforms
    supported = engine.get_supported_platforms()
    print(f"Supported platforms: {supported}")
    
    # Get platform stats
    stats = engine.get_platform_stats()
    print(f"\nPlatform Statistics:")
    print(f"   Total platforms: {stats['total_platforms']}")
    print(f"   Available handlers: {stats['available_handlers']}")
    
    print(f"\nPlatform Details:")
    for platform, info in stats['platforms'].items():
        status = "✅" if info['available'] else "❌"
        print(f"   {status} {platform.upper():12} - {info.get('handler_class', 'Not available')}")
    
    # Test routing with mock jobs
    print(f"\n🎯 Testing Application Routing:")
    print("-" * 60)
    
    mock_jobs = [
        {
            "url": "https://www.linkedin.com/jobs/view/python-dev/",
            "company": "TechCorp",
            "title": "Python Developer"
        },
        {
            "url": "https://jobs.lever.co/techcorp/backend-dev/",
            "company": "TechCorp", 
            "title": "Backend Developer"
        }
    ]
    
    for job in mock_jobs:
        print(f"\nJob: {job['title']} at {job['company']}")
        print(f"URL: {job['url']}")
        
        # Detect platform
        platform = engine.platform_detector.detect(job['url'])
        print(f"Detected platform: {platform}")
        
        # Check handler availability
        handler = engine.handlers.get(platform)
        if handler:
            print(f"Handler available: ✅ {handler.__class__.__name__}")
        else:
            print(f"Handler available: ❌ Not implemented")


def test_architecture_flow():
    """Demonstrate the new architecture flow"""
    print("\n🚀 NEW ARCHITECTURE FLOW DEMONSTRATION")
    print("=" * 60)
    
    print("📋 OLD ARCHITECTURE:")
    print("   Job → LinkedInApply()")
    print("   ❌ Only supports LinkedIn")
    print("   ❌ No platform detection")
    print("   ❌ No flexibility")
    
    print("\n📋 NEW ARCHITECTURE:")
    print("   Job → ApplyEngine")
    print("        ↓")
    print("   PlatformDetector")
    print("        ↓")
    print("   Correct ATS Handler")
    print("        ↓")
    print("   Platform-Specific Apply")
    
    print("\n🎯 PLATFORM ROUTING:")
    print("-" * 60)
    
    routing_map = {
        "linkedin.com": "linkedin",
        "workday": "workday",
        "greenhouse": "greenhouse",
        "lever.co": "lever",
        "indeed.com": "indeed"
    }
    
    for url_pattern, platform in routing_map.items():
        handler_name = f"{platform.capitalize()}Handler"
        print(f"   {url_pattern:20} → {platform.upper():12} → {handler_name}")
    
    print("\n✅ BENEFITS:")
    print("   • Multi-platform support")
    print("   • Automatic platform detection")
    print("   • Platform-specific optimization")
    print("   • Easy to add new platforms")
    print("   • Consistent interface")
    print("   • Graceful fallbacks")
    
    print("\n🔧 EXTENSIBILITY:")
    print("-" * 60)
    print("   To add a new platform:")
    print("   1. Create handler in agents/handlers/")
    print("   2. Inherit from BaseATSHandler")
    print("   3. Implement apply() method")
    print("   4. Add detection rule to PlatformDetector")
    print("   5. Register in ApplyEngine")
    print("   6. No changes to existing code!")


def test_real_world_scenario():
    """Test real-world scenario with mixed job sources"""
    print("\n🧪 REAL-WORLD SCENARIO TEST")
    print("=" * 60)
    
    # Simulate jobs from different sources
    job_feed = [
        {
            "url": "https://www.linkedin.com/jobs/view/python-developer-123/",
            "company": "Google",
            "title": "Python Developer"
        },
        {
            "url": "https://myworkdayjobs.com/amazon/job/backend-dev",
            "company": "Amazon",
            "title": "Backend Developer"
        },
        {
            "url": "https://boards.greenhouse.io/stripe/jobs/456",
            "company": "Stripe",
            "title": "Software Engineer"
        },
        {
            "url": "https://jobs.lever.co/netflix/engineering",
            "company": "Netflix",
            "title": "Senior Engineer"
        },
        {
            "url": "https://www.indeed.com/viewjob?jk=python",
            "company": "Startup",
            "title": "Python Developer"
        }
    ]
    
    detector = PlatformDetector()
    engine = ApplyEngine()
    
    print(f"Processing {len(job_feed)} jobs from different platforms:")
    print("-" * 60)
    
    platform_counts = {}
    
    for job in job_feed:
        platform = detector.detect(job['url'])
        platform_counts[platform] = platform_counts.get(platform, 0) + 1
        
        handler = engine.handlers.get(platform)
        handler_status = "✅" if handler else "⚠️"
        
        print(f"{job['company']:15} {job['title']:20} → {platform.upper():12} {handler_status}")
    
    print(f"\n📊 Platform Distribution:")
    for platform, count in platform_counts.items():
        print(f"   {platform.upper():12}: {count} jobs")
    
    supported = engine.get_supported_platforms()
    print(f"\n🎯 Application Readiness:")
    print(f"   Ready for: {len(supported)} platforms")
    print(f"   Pending: {len(platform_counts) - len(supported)} platforms")


def main():
    """Run all architecture tests"""
    print("🧱 NEW ARCHITECTURE TESTS")
    print("=" * 60)
    
    # Test platform detector
    detector_success = test_platform_detector()
    
    # Test apply engine
    test_apply_engine()
    
    # Demonstrate architecture flow
    test_architecture_flow()
    
    # Test real-world scenario
    test_real_world_scenario()
    
    print("\n" + "=" * 60)
    print("✅ ARCHITECTURE TESTS COMPLETE")
    print("\n🎯 NEW ARCHITECTURE BENEFITS:")
    print("   ✅ Multi-platform support")
    print("   ✅ Automatic platform detection")
    print("   ✅ Extensible handler system")
    print("   ✅ Consistent application interface")
    print("   ✅ Easy to add new platforms")
    print("   ✅ Platform-specific optimization")


if __name__ == "__main__":
    main()
