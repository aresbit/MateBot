/**
 * 审查选项
 */
export interface ReviewOptions {
  // 输入源（三选一）
  mrUrl?: string;              // GitLab/GitHub MR URL
  diffFile?: string;           // Git diff 文件路径
  fileChanges?: FileChange[];  // 直接提供文件变更

  // 分析深度
  depth?: 'quick' | 'standard' | 'deep';

  // 审查重点（可选，默认全部）
  focus?: ReviewFocus[];

  // 输出格式
  output?: 'markdown' | 'json' | 'console' | 'mr-comment';

  // 输出路径
  outputPath?: string;
}

/**
 * 审查重点类别
 */
export interface ReviewFocus {
  category: 'arkts' | 'performance' | 'api' | 'security' | 'architecture';
  rules?: string[]; // 指定启用的规则ID
}

/**
 * 文件变更
 */
export interface FileChange {
  path: string;
  oldContent?: string;
  newContent: string;
  changeType: 'added' | 'modified' | 'deleted';
}

/**
 * 代码特征（AST 提取）
 */
export interface CodeFeatures {
  // 组件特征
  components: ComponentFeature[];
  // 装饰器使用
  decorators: DecoratorUsage[];
  // API 调用
  apiCalls: ApiCall[];
  // 性能风险点
  performanceRisks: PerformanceRisk[];
}

/**
 * 组件特征
 */
export interface ComponentFeature {
  name: string;
  type: 'page' | 'component' | 'service';
  lifecycle: {
    hasAboutToAppear: boolean;
    hasAboutToDisappear: boolean;
  };
  stateManagement: {
    stateVars: number;
    propVars: number;
    linkVars: number;
  };
}

/**
 * 装饰器使用
 */
export interface DecoratorUsage {
  type: '@State' | '@Prop' | '@Link' | '@Provide' | '@Consume' | '@Watch' | '@Reusable';
  line: number;
  target: string;
}

/**
 * API 调用
 */
export interface ApiCall {
  api: string;
  module: string;
  line: number;
  hasPermissionCheck: boolean;
  hasErrorHandling: boolean;
}

/**
 * 性能风险点
 */
export interface PerformanceRisk {
  type: 'large-list' | 'no-key' | 'complex-build' | 'memory-leak' | 'expensive-computation';
  line: number;
  description: string;
}

/**
 * 规则检查结果
 */
export interface RuleIssue {
  id: string;
  rule: string;
  severity: 'critical' | 'high' | 'medium' | 'low' | 'info';
  category: 'arkts' | 'performance' | 'api' | 'security' | 'architecture';
  file: string;
  line: number;
  message: string;
  confidence: number; // 0-1
  fix?: CodeFix;
}

/**
 * 代码修复建议
 */
export interface CodeFix {
  description: string;
  codeSnippet: string;
  verification?: string;
  estimatedTime?: string; // 如 "30 分钟"
}

/**
 * 静态分析结果
 */
export interface StaticAnalysisResult {
  issues: RuleIssue[];
  metrics: CodeMetrics;
  features: CodeFeatures;
  analysisTime: number;
}

/**
 * 代码指标
 */
export interface CodeMetrics {
  totalFiles: number;
  totalLines: number;
  addedLines: number;
  deletedLines: number;
  complexity: number;
}

/**
 * 深度分析结果
 */
export interface AIAnalysisResult {
  architectureAssessment: ArchitectureAssessment;
  performanceRisks: PerformanceRiskDetail[];
  detailedSuggestions: DetailedSuggestion[];
  analysisTime: number;
}

/**
 * 架构评估
 */
export interface ArchitectureAssessment {
  score: number; // 0-100
  layering: {
    hasBusinessLogicInUI: boolean;
    serviceResponsibility: boolean;
    dataLayerIsolation: boolean;
  };
  dependencies: {
    hasCircularDeps: boolean;
    dependencyDirection: 'correct' | 'inverted' | 'mixed';
  };
  coupling: {
    componentComplexity: number;
    stateManagementComplexity: number;
  };
}

/**
 * 性能风险详情
 */
export interface PerformanceRiskDetail {
  type: string;
  severity: 'critical' | 'high' | 'medium' | 'low';
  description: string;
  impact: string;
  recommendation: string;
  codeExample?: string;
}

/**
 * 详细建议
 */
export interface DetailedSuggestion {
  title: string;
  priority: 'critical' | 'high' | 'medium' | 'low';
  description: string;
  codeBefore?: string;
  codeAfter?: string;
  explanation: string;
  references: string[];
}

/**
 * 审查报告
 */
export interface ReviewReport {
  summary: ReportSummary;
  issues: RuleIssue[];
  deepAnalysis?: AIAnalysisResult;
  advantages: string[];
  metadata: ReportMetadata;
}

/**
 * 报告摘要
 */
export interface ReportSummary {
  mrInfo?: {
    url: string;
    branch: string;
    targetBranch: string;
  };
  changes: {
    files: number;
    addedLines: number;
    deletedLines: number;
  };
  analysis: {
    phases: string[];
    duration: number;
  };
  assessment: {
    score: number;
    grade: string;
    critical: number;
    high: number;
    medium: number;
    low: number;
  };
}

/**
 * 报告元数据
 */
export interface ReportMetadata {
  generatedAt: string;
  toolVersion: string;
  analysisDepth: string;
  focusAreas: string[];
}

/**
 * 规则定义
 */
export interface Rule {
  id: string;
  name: string;
  category: 'arkts' | 'performance' | 'api' | 'security' | 'architecture';
  severity: 'critical' | 'high' | 'medium' | 'low';
  description: string;

  check(
    ast: any, // TypeScript SourceFile
    features: CodeFeatures,
    context: CheckContext
  ): RuleCheckResult;
}

/**
 * 规则检查上下文
 */
export interface CheckContext {
  filePath: string;
  fileContent: string;
  repoPath?: string;
  config: Record<string, any>;
}

/**
 * 规则检查结果
 */
export interface RuleCheckResult {
  passed: boolean;
  issues: Omit<RuleIssue, 'id' | 'rule' | 'category'>[];
}

/**
 * 报告生成器接口
 */
export interface Reporter {
  generate(report: ReviewReport): Promise<GeneratedReport>;
}

/**
 * 生成的报告
 */
export interface GeneratedReport {
  format: string;
  content: string;
  metadata: {
    generatedAt: string;
    analysisTime: number;
    issuesCount: number;
  };
}
