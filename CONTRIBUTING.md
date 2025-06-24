# Contributing to RaiderBot - Palantir Foundry

Thank you for your interest in contributing to RaiderBot! This project is built entirely on Palantir Foundry, so all contributions must follow Foundry development practices.

## 🐕 Code of Conduct

Like a loyal German Shepherd, we value:
- **Reliability**: Code that works consistently
- **Safety**: Always prioritize the 60mph limit
- **Teamwork**: Collaborative development
- **Alertness**: Proactive issue identification

## 🔧 Development Setup

### Prerequisites
1. Access to Raider Express Foundry workspace
2. Foundry CLI installed and configured
3. Understanding of Foundry's development model

### Local Development
```bash
# Clone the repository
git clone https://github.com/raider-express/raiderbot-palantir-foundry.git

# Install dependencies
pip install -r requirements.txt

# Test locally before Foundry deployment
open testing/local-dev-setup.html
```

## 📝 Contribution Process

### 1. Foundry Workspace Branch
All development happens in Foundry workspaces:
```bash
foundry workspace create feature/your-feature-name
```

### 2. Code Standards

#### Palantir Foundry Best Practices
- Use Foundry's type system for all objects
- Leverage Foundry Functions for business logic
- Keep transforms idempotent and efficient
- Document all Foundry-specific configurations

#### Python Style
- Follow PEP 8
- Add type hints for Foundry objects
- Include docstrings with Foundry context

#### Safety Requirements
- All code must respect 60mph speed limits
- Safety validations are non-negotiable
- Include safety checks in all vehicle-related functions

### 3. Testing Requirements

```bash
# Run local tests
pytest tests/

# Test Foundry functions
foundry functions test palantir-functions/

# Validate transforms
foundry transforms validate palantir-transforms/
```

### 4. Pull Request Process

1. **Create PR with clear description**
   - What changes were made
   - Which Foundry components affected
   - Safety implications considered

2. **Required Checks**
   - [ ] Code follows Foundry patterns
   - [ ] Tests pass in Foundry workspace
   - [ ] Documentation updated
   - [ ] 60mph compliance maintained

3. **Review Process**
   - Foundry workspace review required
   - Safety team approval for vehicle logic
   - Performance validation on Foundry

## 🚀 Foundry-Specific Guidelines

### Ontology Changes
- Coordinate with data governance team
- Update all dependent functions
- Version ontology changes properly

### Function Development
- Use appropriate memory limits
- Implement proper error handling
- Add Foundry monitoring tags

### Transform Optimization
- Minimize dataset scans
- Use incremental processing
- Monitor resource usage

## 📚 Resources

- [Palantir Foundry Docs](https://docs.palantir.com/foundry)
- [RaiderBot Architecture](documentation/FOUNDRY_ARCHITECTURE.md)
- [API Reference](documentation/API_REFERENCE.md)

## 🤝 Getting Help

- **Foundry Issues**: #foundry-help in Slack
- **RaiderBot Questions**: raiderbot-dev@raiderexpress.com
- **Safety Concerns**: safety-team@raiderexpress.com

---

🐕 Remember: Every contribution makes RaiderBot a better German Shepherd assistant for the Raider Express family!
