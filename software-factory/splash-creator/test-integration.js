#!/usr/bin/env node

/**
 * Comprehensive Integration Test for Splash Creator API
 * 
 * This script tests the entire workflow end-to-end to ensure
 * the real implementation actually works before celebrating.
 */

const BASE_URL = 'http://localhost:3001';

async function testAPI() {
  console.log('🧪 Starting comprehensive integration test...\n');
  
  let allTestsPassed = true;
  const results = {
    projects: false,
    designTokens: false,
    runSubmission: false,
    runStatus: false,
    variantApproval: false,
    pythonExecution: false
  };

  try {
    // Test 1: Projects API
    console.log('1️⃣ Testing Projects API...');
    const projectsResponse = await fetch(`${BASE_URL}/api/projects`);
    const projectsData = await projectsResponse.json();
    
    if (projectsResponse.ok && projectsData.projects && projectsData.projects.length > 0) {
      console.log('   ✅ Projects API working - found', projectsData.projects.length, 'projects');
      results.projects = true;
    } else {
      console.log('   ❌ Projects API failed');
      allTestsPassed = false;
    }

    // Test 2: Design Tokens API
    console.log('\n2️⃣ Testing Design Tokens API...');
    const designResponse = await fetch(`${BASE_URL}/api/projects/weight-tracker-nextjs/design`);
    const designData = await designResponse.json();
    
    if (designResponse.ok && designData.designTokens && designData.designTokens.palette) {
      console.log('   ✅ Design Tokens API working - found', designData.designTokens.palette.length, 'colors');
      results.designTokens = true;
    } else {
      console.log('   ❌ Design Tokens API failed');
      allTestsPassed = false;
    }

    // Test 3: Run Submission API
    console.log('\n3️⃣ Testing Run Submission API...');
    const runData = {
      projectId: 'weight-tracker-nextjs',
      projectName: 'Weight Tracker Pro',
      tone: 'confident',
      primaryHeadline: 'Transform Your Life',
      callToActionPrimary: 'Get Started'
    };
    
    const submitResponse = await fetch(`${BASE_URL}/api/runs`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(runData)
    });
    
    const submitResult = await submitResponse.json();
    
    if (submitResponse.ok && submitResult.runId && submitResult.status === 'pending') {
      console.log('   ✅ Run Submission API working - created run:', submitResult.runId);
      results.runSubmission = true;
      
      // Test 4: Wait for Python execution and check status
      console.log('\n4️⃣ Testing Python Execution and Run Status...');
      console.log('   ⏳ Waiting for Python workflow to complete (up to 30 seconds)...');
      
      let attempts = 0;
      let runComplete = false;
      
      while (attempts < 30 && !runComplete) {
        await new Promise(resolve => setTimeout(resolve, 1000));
        attempts++;
        
        const statusResponse = await fetch(`${BASE_URL}/api/runs/${submitResult.runId}`);
        const statusData = await statusResponse.json();
        
        if (statusResponse.ok) {
          console.log(`   📊 Status check ${attempts}/30: ${statusData.status}`);
          
          if (statusData.status === 'complete') {
            console.log('   ✅ Python execution completed successfully!');
            console.log('   📊 Generated', statusData.artifacts?.length || 0, 'artifacts');
            results.pythonExecution = true;
            results.runStatus = true;
            runComplete = true;
          } else if (statusData.status === 'failed') {
            console.log('   ❌ Python execution failed');
            allTestsPassed = false;
            break;
          }
        } else {
          console.log('   ❌ Run Status API failed');
          allTestsPassed = false;
          break;
        }
      }
      
      if (!runComplete && attempts >= 30) {
        console.log('   ⚠️  Python execution timed out after 30 seconds');
        allTestsPassed = false;
      }
      
      // Test 5: Variant Approval (if we have artifacts)
      if (runComplete) {
        // Get the final status data for variant approval test
        const finalStatusResponse = await fetch(`${BASE_URL}/api/runs/${submitResult.runId}`);
        const finalStatusData = await finalStatusResponse.json();
        
        if (finalStatusData.artifacts && finalStatusData.artifacts.length > 0) {
        console.log('\n5️⃣ Testing Variant Approval API...');
        
        const approveResponse = await fetch(`${BASE_URL}/api/runs/${submitResult.runId}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ variantId: 'variant-1' })
        });
        
        if (approveResponse.ok) {
          console.log('   ✅ Variant Approval API working');
          results.variantApproval = true;
          
          // Verify approval was recorded
          const verifyResponse = await fetch(`${BASE_URL}/api/runs/${submitResult.runId}`);
          const verifyData = await verifyResponse.json();
          
          if (verifyData.artifacts?.[0]?.approved) {
            console.log('   ✅ Variant approval recorded successfully');
          } else {
            console.log('   ❌ Variant approval not recorded');
            allTestsPassed = false;
          }
        } else {
          console.log('   ❌ Variant Approval API failed');
          allTestsPassed = false;
        }
        } else {
          console.log('   ⚠️  No artifacts available for approval test');
        }
      }
      
    } else {
      console.log('   ❌ Run Submission API failed');
      allTestsPassed = false;
    }

  } catch (error) {
    console.log('   ❌ Test failed with error:', error.message);
    allTestsPassed = false;
  }

  // Final Results
  console.log('\n' + '='.repeat(60));
  console.log('📊 INTEGRATION TEST RESULTS');
  console.log('='.repeat(60));
  
  const testNames = {
    projects: 'Projects API',
    designTokens: 'Design Tokens API', 
    runSubmission: 'Run Submission API',
    runStatus: 'Run Status API',
    variantApproval: 'Variant Approval API',
    pythonExecution: 'Python Execution'
  };
  
  Object.entries(results).forEach(([key, passed]) => {
    console.log(`${passed ? '✅' : '❌'} ${testNames[key]}`);
  });
  
  console.log('='.repeat(60));
  
  if (allTestsPassed) {
    console.log('🎉 ALL TESTS PASSED! Implementation is fully working!');
    console.log('✅ Ready for production use');
    process.exit(0);
  } else {
    console.log('💥 SOME TESTS FAILED! Implementation needs fixes.');
    console.log('❌ Not ready for production');
    process.exit(1);
  }
}

// Run the test
testAPI().catch(error => {
  console.error('💥 Test runner failed:', error);
  process.exit(1);
});
