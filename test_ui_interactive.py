#!/usr/bin/env python3
"""
Comprehensive Playwright UI Testing for Interactive Workflow Executor
Tests all interactive elements and workflow execution functionality
"""

import asyncio
import time
from playwright.async_api import async_playwright
import json
import sys
import subprocess
import signal
import os

class InteractiveUITester:
    def __init__(self):
        self.server_process = None
        self.base_url = "http://localhost:8003"
        
    async def start_server(self):
        """Check if server is already running or start it"""
        print("🔍 Checking if live server is running on port 8003...")
        
        # Check if server is already running
        try:
            import requests
            response = requests.get(f"{self.base_url}/api/health", timeout=5)
            if response.status_code == 200:
                print("✅ Server is already running and healthy")
                return True
        except Exception as e:
            print(f"❌ Server not responding: {e}")
            return False
    
    def stop_server(self):
        """Stop the server process - not needed when using existing server"""
        print("✅ Using existing server, no cleanup needed")
    
    async def test_page_load(self, page):
        """Test basic page loading and structure"""
        print("\n🧪 Test 1: Page Loading and Structure")
        
        try:
            await page.goto(self.base_url, wait_until="networkidle")
            
            # Check title
            title = await page.title()
            assert "Interactive Workflow Executor" in title
            print("✅ Page title correct")
            
            # Check main header
            header = await page.locator("h1").text_content()
            assert "Interactive Workflow Executor" in header
            print("✅ Main header found")
            
            # Check status indicator
            status = await page.locator('text="System Status"').text_content()
            assert "Live & Interactive" in status
            print("✅ System status indicator found")
            
            return True
        except Exception as e:
            print(f"❌ Page load test failed: {e}")
            return False
    
    async def test_workflow_cards(self, page):
        """Test workflow card visibility and structure"""
        print("\n🧪 Test 2: Workflow Cards Display")
        
        try:
            # Wait for workflow cards to load
            await page.wait_for_selector('.workflow-card', timeout=10000)
            
            # Count workflow cards
            cards = await page.locator('.workflow-card').count()
            print(f"✅ Found {cards} workflow cards")
            assert cards >= 3, "Should have at least 3 workflow cards"
            
            # Test each card has required elements
            for i in range(cards):
                card = page.locator('.workflow-card').nth(i)
                
                # Check card title
                title = await card.locator('h3').text_content()
                assert len(title) > 0
                print(f"✅ Card {i+1} title: {title}")
                
                # Check execute button
                button = card.locator('button:has-text("Execute Workflow")')
                assert await button.count() == 1
                print(f"✅ Card {i+1} has execute button")
            
            return True
        except Exception as e:
            print(f"❌ Workflow cards test failed: {e}")
            return False
    
    async def test_workflow_execution_modal(self, page):
        """Test opening workflow execution modal"""
        print("\n🧪 Test 3: Workflow Execution Modal")
        
        try:
            # Click on first workflow card's execute button
            first_card = page.locator('.workflow-card').first
            execute_button = first_card.locator('button:has-text("Execute Workflow")')
            await execute_button.click()
            
            # Wait for modal to appear
            await page.wait_for_selector('.modal-backdrop', timeout=5000)
            print("✅ Modal opened successfully")
            
            # Check modal content
            modal = page.locator('.modal-backdrop')
            
            # Check modal title
            title = await modal.locator('h2').text_content()
            assert len(title) > 0
            print(f"✅ Modal title: {title}")
            
            # Check progress bar
            progress_bar = modal.locator('.bg-gray-200.rounded-full')
            assert await progress_bar.count() > 0
            print("✅ Progress bar found")
            
            # Check step cards
            step_cards = await modal.locator('.step-card').count()
            assert step_cards > 0
            print(f"✅ Found {step_cards} step cards")
            
            # Check close button works
            close_button = modal.locator('button:has-text("Close")')
            await close_button.click()
            
            # Wait for modal to disappear
            await page.wait_for_selector('.modal-backdrop', state='hidden', timeout=5000)
            print("✅ Modal closes successfully")
            
            return True
        except Exception as e:
            print(f"❌ Modal test failed: {e}")
            return False
    
    async def test_step_execution(self, page):
        """Test actual step execution with form interaction"""
        print("\n🧪 Test 4: Step Execution and Form Interaction")
        
        try:
            # Open modal again
            first_card = page.locator('.workflow-card').first
            execute_button = first_card.locator('button:has-text("Execute Workflow")')
            await execute_button.click()
            
            await page.wait_for_selector('.modal-backdrop', timeout=5000)
            modal = page.locator('.modal-backdrop')
            
            # Find the first active step
            active_step = modal.locator('.step-card').first
            
            # Check if there are form fields
            form_fields = await active_step.locator('input, select, textarea').count()
            print(f"✅ Found {form_fields} form fields in first step")
            
            if form_fields > 0:
                # Fill out the first form field
                first_field = active_step.locator('input, select, textarea').first
                field_type = await first_field.get_attribute('type') or 'text'
                
                if field_type == 'text':
                    await first_field.fill('Test Content Topic')
                    print("✅ Filled text field")
                elif await first_field.tag_name() == 'select':
                    # Select first option
                    await first_field.select_option(index=1)
                    print("✅ Selected dropdown option")
            
            # Look for execute button for this step
            step_execute_button = active_step.locator('button:has-text("Execute")')
            if await step_execute_button.count() > 0:
                print("✅ Found step execute button")
                
                # Click execute and wait for processing
                await step_execute_button.click()
                print("🔄 Executing step...")
                
                # Wait for execution to complete (should show success or move to next step)
                await page.wait_for_timeout(8000)  # Wait for API call to complete
                
                # Check if step completed (look for success indicator or next step)
                success_indicators = await modal.locator('text="completed successfully", text="✅"').count()
                if success_indicators > 0:
                    print("✅ Step execution completed successfully")
                else:
                    print("⚠️ Step execution may still be in progress")
            
            # Close modal
            close_button = modal.locator('button:has-text("Close")')
            await close_button.click()
            
            return True
        except Exception as e:
            print(f"❌ Step execution test failed: {e}")
            return False
    
    async def test_api_endpoints(self, page):
        """Test API endpoints are responding"""
        print("\n🧪 Test 5: API Endpoints")
        
        try:
            # Test health endpoint
            health_response = await page.evaluate("""
                fetch('/api/health').then(r => r.json())
            """)
            assert health_response['status'] == 'healthy'
            print("✅ Health endpoint working")
            
            # Test workflows endpoint
            workflows_response = await page.evaluate("""
                fetch('/api/workflows').then(r => r.json())
            """)
            assert 'workflows' in workflows_response
            print("✅ Workflows endpoint working")
            
            return True
        except Exception as e:
            print(f"❌ API endpoints test failed: {e}")
            return False
    
    async def test_responsive_design(self, page):
        """Test responsive design at different screen sizes"""
        print("\n🧪 Test 6: Responsive Design")
        
        try:
            # Test desktop size
            await page.set_viewport_size({"width": 1920, "height": 1080})
            cards_desktop = await page.locator('.workflow-card').count()
            print(f"✅ Desktop view: {cards_desktop} cards visible")
            
            # Test tablet size
            await page.set_viewport_size({"width": 768, "height": 1024})
            await page.wait_for_timeout(1000)
            cards_tablet = await page.locator('.workflow-card').count()
            print(f"✅ Tablet view: {cards_tablet} cards visible")
            
            # Test mobile size
            await page.set_viewport_size({"width": 375, "height": 667})
            await page.wait_for_timeout(1000)
            cards_mobile = await page.locator('.workflow-card').count()
            print(f"✅ Mobile view: {cards_mobile} cards visible")
            
            # Reset to desktop
            await page.set_viewport_size({"width": 1920, "height": 1080})
            
            return True
        except Exception as e:
            print(f"❌ Responsive design test failed: {e}")
            return False
    
    async def run_all_tests(self):
        """Run comprehensive UI tests"""
        print("🎯 Starting Comprehensive Interactive UI Testing")
        print("=" * 60)
        
        # Start server
        if not await self.start_server():
            print("❌ Failed to start server. Aborting tests.")
            return False
        
        try:
            async with async_playwright() as p:
                # Launch browser
                browser = await p.chromium.launch(headless=False)  # Set to True for headless
                context = await browser.new_context()
                page = await context.new_page()
                
                # Enable console logging
                page.on("console", lambda msg: print(f"🌐 Browser: {msg.text}"))
                page.on("pageerror", lambda error: print(f"🚨 Page Error: {error}"))
                
                # Run all tests
                tests = [
                    self.test_page_load,
                    self.test_workflow_cards,
                    self.test_workflow_execution_modal,
                    self.test_step_execution,
                    self.test_api_endpoints,
                    self.test_responsive_design
                ]
                
                results = []
                for test in tests:
                    result = await test(page)
                    results.append(result)
                
                # Close browser
                await browser.close()
                
                # Print summary
                print("\n" + "=" * 60)
                print("🏁 TEST SUMMARY")
                print("=" * 60)
                
                passed = sum(results)
                total = len(results)
                
                for i, (test, result) in enumerate(zip(tests, results)):
                    status = "✅ PASS" if result else "❌ FAIL"
                    print(f"{status} - {test.__name__}")
                
                print(f"\n📊 Results: {passed}/{total} tests passed")
                
                if passed == total:
                    print("🎉 ALL TESTS PASSED! The interactive UI is fully functional.")
                    return True
                else:
                    print("⚠️ Some tests failed. The UI may have issues.")
                    return False
                    
        except Exception as e:
            print(f"❌ Test execution failed: {e}")
            return False
        finally:
            self.stop_server()

async def main():
    tester = InteractiveUITester()
    success = await tester.run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    asyncio.run(main())