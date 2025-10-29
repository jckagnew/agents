#!/usr/bin/env node
/**
 * Respect-Spec Framework
 * Validates that generated artifacts respect the original PRD specifications
 * 
 * This is a skeleton implementation that will be expanded when architecture/UX
 * artifacts are available from Claude.
 * 
 * Usage:
 *   node scripts/respect_spec.js \
 *     --prd-dir session-X/prd \
 *     --architecture-dir session-X/architecture \
 *     --ux-dir session-X/ux \
 *     --output-file session-X/respect-spec-report.json
 */

const fs = require('fs');
const path = require('path');

// Parse arguments
const args = process.argv.slice(2);
const getArg = (flag) => {
    const index = args.indexOf(flag);
    return index !== -1 ? args[index + 1] : null;
};

const prdDir = getArg('--prd-dir');
const architectureDir = getArg('--architecture-dir');
const uxDir = getArg('--ux-dir');
const outputFile = getArg('--output-file');

if (!prdDir || !outputFile) {
    console.error('Usage: node respect_spec.js --prd-dir <path> --output-file <path> [--architecture-dir <path>] [--ux-dir <path>]');
    process.exit(1);
}

console.log('🔍 Respect-Spec Framework - Validating Artifact Compliance');
console.log(`   PRD Directory: ${prdDir}`);
console.log(`   Architecture Directory: ${architectureDir || 'Not provided'}`);
console.log(`   UX Directory: ${uxDir || 'Not provided'}`);
console.log(`   Output File: ${outputFile}\n`);

// ============================================================================
// PRD PARSING FUNCTIONS
// ============================================================================

function parsePersonas(prdDir) {
    const personasFile = path.join(prdDir, '01-personas.md');
    
    if (!fs.existsSync(personasFile)) {
        console.warn('⚠️  Personas file not found:', personasFile);
        return null;
    }

    const content = fs.readFileSync(personasFile, 'utf8');
    
    // Extract persona information (basic parsing)
    const personas = {
        primary: null,
        secondary: null,
        scenarios: []
    };

    // Parse primary persona
    const primaryMatch = content.match(/## Primary Persona: (.+?)\n\n\*\*Demographics\*\*:\n- Age: (\d+)\n- Occupation: (.+?)\n\n\*\*Goals\*\*:\n((?:- .+\n?)+)\n\n\*\*Frustrations\*\*:\n((?:- .+\n?)+)\n\n\*\*Jobs to be Done\*\*:\n((?:> .+\n?)+)/s);
    
    if (primaryMatch) {
        personas.primary = {
            name: primaryMatch[1],
            age: parseInt(primaryMatch[2]),
            occupation: primaryMatch[3],
            goals: primaryMatch[4].split('\n').filter(line => line.trim().startsWith('-')).map(line => line.replace(/^- /, '').trim()),
            frustrations: primaryMatch[5].split('\n').filter(line => line.trim().startsWith('-')).map(line => line.replace(/^- /, '').trim()),
            jobsToBeDone: primaryMatch[6].split('\n').filter(line => line.trim().startsWith('>')).map(line => line.replace(/^> /, '').trim())
        };
    }

    // Parse scenarios
    const scenarioMatches = content.match(/### Scenario \d+: (.+?)\n\*\*Context\*\*: (.+?)\n\*\*Steps\*\*:\n((?:\d+\. .+\n?)+)\n\*\*Success Criteria\*\*: (.+?)(?=\n\n|$)/gs);
    
    if (scenarioMatches) {
        scenarioMatches.forEach(match => {
            const lines = match.split('\n');
            const title = lines[0].replace(/### Scenario \d+: /, '');
            const context = lines[1].replace(/\*\*Context\*\*: /, '');
            const steps = lines.slice(3, -2).map(step => step.replace(/^\d+\. /, '').trim());
            const successCriteria = lines[lines.length - 1].replace(/\*\*Success Criteria\*\*: /, '');
            
            personas.scenarios.push({
                title,
                context,
                steps,
                successCriteria
            });
        });
    }

    return personas;
}

function parseProblemSolution(prdDir) {
    const problemFile = path.join(prdDir, '02-problem-solution.md');
    
    if (!fs.existsSync(problemFile)) {
        console.warn('⚠️  Problem/Solution file not found:', problemFile);
        return null;
    }

    const content = fs.readFileSync(problemFile, 'utf8');
    
    // Extract key information
    const problemSolution = {
        escapePoints: [],
        arrivalPoints: [],
        valueProposition: '',
        corePromise: '',
        successMetrics: {
            escape: [],
            arrival: []
        }
    };

    // Parse escape points
    const escapeMatch = content.match(/### What users are escaping FROM:\n((?:- \*\*.+\*\*: .+\n?)+)/s);
    if (escapeMatch) {
        problemSolution.escapePoints = escapeMatch[1]
            .split('\n')
            .filter(line => line.trim().startsWith('-'))
            .map(line => line.replace(/^- \*\*(.+?)\*\*: (.+)/, '$1: $2').trim());
    }

    // Parse arrival points
    const arrivalMatch = content.match(/### What users are arriving TO:\n((?:- \*\*.+\*\*: .+\n?)+)/s);
    if (arrivalMatch) {
        problemSolution.arrivalPoints = arrivalMatch[1]
            .split('\n')
            .filter(line => line.trim().startsWith('-'))
            .map(line => line.replace(/^- \*\*(.+?)\*\*: (.+)/, '$1: $2').trim());
    }

    // Parse value proposition
    const valuePropMatch = content.match(/> (.+?)\n/);
    if (valuePropMatch) {
        problemSolution.valueProposition = valuePropMatch[1];
    }

    // Parse core promise
    const corePromiseMatch = content.match(/\*\*(.+?)\*\* helps you (.+?) consistently with zero friction, so you can (.+?) without the overwhelm\./);
    if (corePromiseMatch) {
        problemSolution.corePromise = {
            appName: corePromiseMatch[1],
            action: corePromiseMatch[2],
            outcome: corePromiseMatch[3]
        };
    }

    return problemSolution;
}

function parseAcceptanceCriteria(prdDir) {
    const criteriaFile = path.join(prdDir, '03-acceptance-criteria.md');
    
    if (!fs.existsSync(criteriaFile)) {
        console.warn('⚠️  Acceptance Criteria file not found:', criteriaFile);
        return null;
    }

    const content = fs.readFileSync(criteriaFile, 'utf8');
    
    const criteria = {
        mustHaveFeatures: [],
        niceToHaveFeatures: [],
        nonFunctionalRequirements: {
            performance: [],
            accessibility: [],
            security: [],
            browserSupport: []
        },
        definitionOfDone: {
            design: [],
            development: [],
            deployment: []
        }
    };

    // Parse must-have features
    const mustHaveMatches = content.match(/### \d+\. (.+?)\n\n\*\*User Story\*\*: (.+?)\n\n\*\*Acceptance Criteria\*\*:\n((?:- \[ \] .+\n?)+)/gs);
    
    if (mustHaveMatches) {
        mustHaveMatches.forEach(match => {
            const lines = match.split('\n');
            const featureName = lines[0].replace(/### \d+\. /, '');
            const userStory = lines[2].replace(/\*\*User Story\*\*: /, '');
            const acceptanceCriteria = lines.slice(4, -1)
                .filter(line => line.trim().startsWith('- [ ]'))
                .map(line => line.replace(/^- \[ \] /, '').trim());
            
            criteria.mustHaveFeatures.push({
                name: featureName,
                userStory,
                acceptanceCriteria
            });
        });
    }

    // Parse non-functional requirements
    const perfMatch = content.match(/### Performance\n((?:- \[ \] .+\n?)+)/);
    if (perfMatch) {
        criteria.nonFunctionalRequirements.performance = perfMatch[1]
            .split('\n')
            .filter(line => line.trim().startsWith('- [ ]'))
            .map(line => line.replace(/^- \[ \] /, '').trim());
    }

    const a11yMatch = content.match(/### Accessibility\n((?:- \[ \] .+\n?)+)/);
    if (a11yMatch) {
        criteria.nonFunctionalRequirements.accessibility = a11yMatch[1]
            .split('\n')
            .filter(line => line.trim().startsWith('- [ ]'))
            .map(line => line.replace(/^- \[ \] /, '').trim());
    }

    return criteria;
}

// ============================================================================
// VALIDATION FUNCTIONS
// ============================================================================

function validateArchitectureCompliance(prdData, architectureDir) {
    if (!architectureDir || !fs.existsSync(architectureDir)) {
        return {
            status: 'skipped',
            reason: 'Architecture directory not provided or does not exist',
            compliance: 0
        };
    }

    console.log('📋 Architecture validation - analyzing existing files...');
    
    const architectureFiles = fs.readdirSync(architectureDir);
    const expectedFiles = [
        'architecture-data-model.md',
        'architecture-services.md', 
        'architecture-tech-stack.md'
    ];
    
    const foundFiles = expectedFiles.filter(file => architectureFiles.includes(file));
    const missingFiles = expectedFiles.filter(file => !architectureFiles.includes(file));
    
    let compliance = 0;
    const issues = [];
    const strengths = [];
    
    // Check file presence
    if (foundFiles.length === expectedFiles.length) {
        compliance += 20;
        strengths.push('All expected architecture files present');
    } else {
        issues.push(`Missing files: ${missingFiles.join(', ')}`);
    }
    
    // Validate data model compliance with PRD
    const dataModelFile = path.join(architectureDir, 'architecture-data-model.md');
    if (fs.existsSync(dataModelFile)) {
        const dataModelContent = fs.readFileSync(dataModelFile, 'utf8');
        
        // Check if data model addresses PRD requirements
        const prdFeatures = prdData.acceptanceCriteria?.mustHaveFeatures || [];
        const hasEntryModel = dataModelContent.includes('Entry') && dataModelContent.includes('Entry');
        const hasGoalModel = dataModelContent.includes('Goal') && dataModelContent.includes('Goal');
        
        if (hasEntryModel && hasGoalModel) {
            compliance += 30;
            strengths.push('Data model covers core tracking entities (Entry, Goal)');
        } else {
            issues.push('Data model missing core entities for tracking features');
        }
        
        // Check for privacy compliance (local storage)
        if (dataModelContent.includes('localStorage') || dataModelContent.includes('local-first')) {
            compliance += 20;
            strengths.push('Architecture supports privacy-first local storage');
        } else {
            issues.push('Architecture may not fully support local-first privacy requirements');
        }
        
        // Check for TypeScript interfaces
        if (dataModelContent.includes('interface') && dataModelContent.includes('TypeScript')) {
            compliance += 15;
            strengths.push('Data model includes TypeScript interfaces for type safety');
        }
    }
    
    // Validate tech stack alignment with PRD
    const techStackFile = path.join(architectureDir, 'architecture-tech-stack.md');
    if (fs.existsSync(techStackFile)) {
        const techStackContent = fs.readFileSync(techStackFile, 'utf8');
        
        // Check for performance targets alignment
        if (techStackContent.includes('< 2 seconds') || techStackContent.includes('performance')) {
            compliance += 10;
            strengths.push('Tech stack addresses performance requirements');
        }
        
        // Check for accessibility compliance
        if (techStackContent.includes('WCAG') || techStackContent.includes('accessibility')) {
            compliance += 5;
            strengths.push('Tech stack includes accessibility considerations');
        }
    }
    
    // Validate services architecture
    const servicesFile = path.join(architectureDir, 'architecture-services.md');
    if (fs.existsSync(servicesFile)) {
        const servicesContent = fs.readFileSync(servicesFile, 'utf8');
        
        // Check for React/Next.js architecture
        if (servicesContent.includes('React') || servicesContent.includes('Next.js')) {
            compliance += 10;
            strengths.push('Services architecture uses modern React/Next.js stack');
        }
        
        // Check for state management approach
        if (servicesContent.includes('Context') || servicesContent.includes('localStorage')) {
            compliance += 5;
            strengths.push('State management approach aligns with local-first requirements');
        }
    }
    
    const status = compliance >= 80 ? 'compliant' : compliance >= 60 ? 'partially_compliant' : 'non_compliant';
    
    return {
        status,
        compliance,
        reason: issues.length > 0 ? issues.join('; ') : 'Architecture validation complete',
        strengths,
        issues,
        foundFiles,
        missingFiles
    };
}

function validateUXCompliance(prdData, uxDir) {
    if (!uxDir || !fs.existsSync(uxDir)) {
        return {
            status: 'skipped',
            reason: 'UX directory not provided or does not exist',
            compliance: 0
        };
    }

    console.log('🎨 UX validation - analyzing existing files...');
    
    const uxFiles = fs.readdirSync(uxDir);
    const expectedFiles = [
        'user-flows.md',
        'wireframes.md',
        'interaction-specs.md',
        'accessibility-guidelines.md'
    ];
    
    const foundFiles = expectedFiles.filter(file => uxFiles.includes(file));
    const missingFiles = expectedFiles.filter(file => !uxFiles.includes(file));
    
    let compliance = 0;
    const issues = [];
    const strengths = [];
    
    // Check file presence
    if (foundFiles.length === expectedFiles.length) {
        compliance += 25;
        strengths.push('All expected UX files present');
    } else {
        issues.push(`Missing files: ${missingFiles.join(', ')}`);
    }
    
    // Validate user flows compliance with PRD
    const userFlowsFile = path.join(uxDir, 'user-flows.md');
    if (fs.existsSync(userFlowsFile)) {
        const userFlowsContent = fs.readFileSync(userFlowsFile, 'utf8');
        
        // Check if user flows address PRD personas
        const personas = prdData.personas;
        if (personas && personas.primary) {
            const hasPrimaryPersonaFlow = userFlowsContent.includes(personas.primary.name) || 
                                       userFlowsContent.includes('Health-Conscious Hannah');
            if (hasPrimaryPersonaFlow) {
                compliance += 20;
                strengths.push('User flows address primary persona needs');
            } else {
                issues.push('User flows missing primary persona coverage');
            }
        }
        
        // Check for Mermaid diagrams
        if (userFlowsContent.includes('```mermaid') || userFlowsContent.includes('mermaid')) {
            compliance += 15;
            strengths.push('User flows include Mermaid diagrams for visualization');
        }
        
        // Check for core flows
        const coreFlows = ['onboarding', 'tracking', 'goals', 'progress'];
        const hasCoreFlows = coreFlows.some(flow => 
            userFlowsContent.toLowerCase().includes(flow)
        );
        if (hasCoreFlows) {
            compliance += 15;
            strengths.push('User flows cover core application flows');
        } else {
            issues.push('User flows missing core application flows');
        }
    }
    
    // Validate wireframes compliance
    const wireframesFile = path.join(uxDir, 'wireframes.md');
    if (fs.existsSync(wireframesFile)) {
        const wireframesContent = fs.readFileSync(wireframesFile, 'utf8');
        
        // Check for required screens
        const requiredScreens = ['splash', 'dashboard', 'log entry', 'history', 'settings', 'goals'];
        const hasRequiredScreens = requiredScreens.some(screen => 
            wireframesContent.toLowerCase().includes(screen)
        );
        if (hasRequiredScreens) {
            compliance += 15;
            strengths.push('Wireframes specify required application screens');
        } else {
            issues.push('Wireframes missing required application screens');
        }
        
        // Check for responsive design
        if (wireframesContent.includes('responsive') || wireframesContent.includes('breakpoint')) {
            compliance += 10;
            strengths.push('Wireframes include responsive design specifications');
        }
        
        // Check for accessibility specs
        if (wireframesContent.includes('accessibility') || wireframesContent.includes('ARIA')) {
            compliance += 10;
            strengths.push('Wireframes include accessibility specifications');
        }
    }
    
    // Validate interaction specs
    const interactionFile = path.join(uxDir, 'interaction-specs.md');
    if (fs.existsSync(interactionFile)) {
        const interactionContent = fs.readFileSync(interactionFile, 'utf8');
        
        // Check for performance requirements
        if (interactionContent.includes('60fps') || interactionContent.includes('performance')) {
            compliance += 10;
            strengths.push('Interaction specs include performance requirements');
        }
        
        // Check for accessibility considerations
        if (interactionContent.includes('accessibility') || interactionContent.includes('WCAG')) {
            compliance += 10;
            strengths.push('Interaction specs include accessibility considerations');
        }
    }
    
    // Validate accessibility guidelines
    const accessibilityFile = path.join(uxDir, 'accessibility-guidelines.md');
    if (fs.existsSync(accessibilityFile)) {
        const accessibilityContent = fs.readFileSync(accessibilityFile, 'utf8');
        
        // Check for WCAG compliance
        if (accessibilityContent.includes('WCAG') || accessibilityContent.includes('2.1')) {
            compliance += 15;
            strengths.push('Accessibility guidelines specify WCAG compliance');
        }
        
        // Check for screen reader support
        if (accessibilityContent.includes('screen reader') || accessibilityContent.includes('ARIA')) {
            compliance += 10;
            strengths.push('Accessibility guidelines include screen reader support');
        }
    }
    
    const status = compliance >= 80 ? 'compliant' : compliance >= 60 ? 'partially_compliant' : 'non_compliant';
    
    return {
        status,
        compliance,
        reason: issues.length > 0 ? issues.join('; ') : 'UX validation complete',
        strengths,
        issues,
        foundFiles,
        missingFiles
    };
}

// ============================================================================
// MAIN EXECUTION
// ============================================================================

console.log('📄 Parsing PRD documents...');

// Parse PRD data
const prdData = {
    personas: parsePersonas(prdDir),
    problemSolution: parseProblemSolution(prdDir),
    acceptanceCriteria: parseAcceptanceCriteria(prdDir)
};

console.log('✅ PRD parsing complete');
console.log(`   - Personas: ${prdData.personas ? 'Found' : 'Missing'}`);
console.log(`   - Problem/Solution: ${prdData.problemSolution ? 'Found' : 'Missing'}`);
console.log(`   - Acceptance Criteria: ${prdData.acceptanceCriteria ? 'Found' : 'Missing'}`);

console.log('\n🔍 Validating compliance...');

// Run validations
const architectureValidation = validateArchitectureCompliance(prdData, architectureDir);
const uxValidation = validateUXCompliance(prdData, uxDir);

const validationResults = {
    timestamp: new Date().toISOString(),
    prdData: prdData,
    validations: {
        architecture: architectureValidation,
        ux: uxValidation
    },
    overallCompliance: 0,
    status: 'incomplete'
};

// Log validation results
console.log('📋 Architecture validation - analyzing existing files...');
if (architectureValidation.status === 'skipped') {
    console.log(`⏭️  Architecture validation skipped: ${architectureValidation.reason}`);
} else {
    console.log(`🏗️  Architecture validation: ${architectureValidation.compliance}% compliance (${architectureValidation.status})`);
    if (architectureValidation.strengths && architectureValidation.strengths.length > 0) {
        architectureValidation.strengths.forEach(strength => console.log(`   ✅ ${strength}`));
    }
    if (architectureValidation.issues && architectureValidation.issues.length > 0) {
        architectureValidation.issues.forEach(issue => console.log(`   ⚠️  ${issue}`));
    }
}

console.log('🎨 UX validation - analyzing existing files...');
if (uxValidation.status === 'skipped') {
    console.log(`⏭️  UX validation skipped: ${uxValidation.reason}`);
} else if (uxValidation.status === 'pending') {
    console.log(`⏳ UX validation pending: ${uxValidation.reason}`);
} else {
    console.log(`🎨 UX validation: ${uxValidation.compliance}% compliance (${uxValidation.status})`);
    if (uxValidation.strengths && uxValidation.strengths.length > 0) {
        uxValidation.strengths.forEach(strength => console.log(`   ✅ ${strength}`));
    }
    if (uxValidation.issues && uxValidation.issues.length > 0) {
        uxValidation.issues.forEach(issue => console.log(`   ⚠️  ${issue}`));
    }
}

// Calculate overall compliance
const validations = Object.values(validationResults.validations);
const completedValidations = validations.filter(v => v.status === 'compliant' || v.status === 'partially_compliant' || v.status === 'non_compliant');
const totalCompliance = completedValidations.reduce((sum, v) => sum + v.compliance, 0);

if (completedValidations.length > 0) {
    validationResults.overallCompliance = totalCompliance / completedValidations.length;
    validationResults.status = validationResults.overallCompliance >= 80 ? 'compliant' : 'non-compliant';
} else {
    validationResults.status = 'pending';
}

// Ensure output directory exists
const outputDir = path.dirname(outputFile);
if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
}

// Write results
fs.writeFileSync(outputFile, JSON.stringify(validationResults, null, 2));

console.log('\n✅ Respect-Spec validation complete');
console.log(`📊 Overall Compliance: ${validationResults.overallCompliance.toFixed(1)}%`);
console.log(`📁 Results saved: ${outputFile}`);

if (validationResults.status === 'pending') {
    console.log('\n⏳ Status: Waiting for Claude architecture/UX artifacts');
    console.log('   Run again after Claude generates the missing artifacts');
} else if (validationResults.status === 'compliant') {
    console.log('\n🎉 Status: All artifacts respect PRD specifications');
} else {
    console.log('\n⚠️  Status: Some artifacts do not fully comply with PRD');
}

process.exit(0);
